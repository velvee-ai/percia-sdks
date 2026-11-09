import { Command } from "commander";
import { signWebhook, type Event } from "@percia/sdk";
import { randomBytes } from "node:crypto";
import type { Context, GlobalOptions } from "../context.js";
import { CliError, EXIT, stripControl } from "../errors.js";
import { isoOrDash, json, ndjson } from "../output.js";
import { openSession } from "../session.js";
import { pollNew, SeenSet } from "./events.js";

type Deps = { ctx: Context; globals: () => GlobalOptions };

/** The documented delivery body (docs/integrators/webhooks.md), rebuilt from an event of the account feed plus the watch's goal. */
export function deliveryBody(e: Event & { watchId?: string }, goal: string) {
	return { id: e.decisionId ?? e.id, watchId: e.watchId, occurrenceId: e.occurrenceId, type: e.type, goal, reason: e.reason, confidence: e.confidence, at: e.at };
}

const isLoopback = (u: URL) => ["localhost", "127.0.0.1", "[::1]", "::1"].includes(u.hostname) || u.hostname.endsWith(".localhost");

export function registerListen(program: Command, { ctx, globals }: Deps) {
	program
		.command("listen")
		.description(
			"Forward new events to a local HTTP endpoint, signed like real deliveries. Polls GET /api/events (Percia cannot reach your localhost), so deliveries are emulated: see docs/cli-listen.md.",
		)
		.requiredOption("--forward <url>", "where to POST each event, e.g. http://localhost:3000/hook")
		.option("--secret <whsec>", "sign with this secret (use your watch's or hook's real secret so your receiver verifies unchanged). Default: PERCIA_WEBHOOK_SECRET, else a generated one printed once")
		.option("--watch <id>", "only events of this watch")
		.option("--replay <n>", "also forward the latest n existing events first", (v) => Number(v), 0)
		.option("--interval <seconds>", "poll interval (minimum 2)", (v) => Number(v), 3)
		.option("--allow-remote", "allow a --forward target that is not localhost")
		.action(async (o: { forward: string; secret?: string; watch?: string; replay: number; interval: number; allowRemote?: boolean }) => {
			const g = globals();
			let target: URL;
			try {
				target = new URL(o.forward);
			} catch {
				throw new CliError(`--forward is not a URL: ${o.forward}`, EXIT.USAGE);
			}
			if (!/^https?:$/.test(target.protocol)) throw new CliError("--forward must be http(s).", EXIT.USAGE);
			if (!isLoopback(target) && !o.allowRemote) throw new CliError("--forward points away from this machine.", EXIT.USAGE, "Pass --allow-remote if that is intended. Event text will be sent there.");

			const { client } = await openSession(ctx, g);
			let secret = o.secret ?? ctx.env.PERCIA_WEBHOOK_SECRET;
			let generated = false;
			if (!secret) {
				secret = `whsec_local_${randomBytes(16).toString("hex")}`;
				generated = true;
			}
			const log = (line: string) => (g.json ? undefined : ctx.stderr(line + "\n"));
			log(`Forwarding new events from ${client.baseUrl} to ${target.origin}${target.pathname}`);
			if (generated) log(`Signing with a local secret (use it in your receiver while testing):\n  ${secret}`);
			else log("Signing with the secret you provided.");
			log("This polls the event feed; it is not a live relay. Ctrl-C to stop.\n");

			const seen = new SeenSet();
			const goals = new Map<string, string>();
			const goalFor = async (watchId: string) => {
				if (goals.has(watchId)) return goals.get(watchId)!;
				let goal = "";
				try {
					goal = ((await client.watches.get(watchId)) as { goal?: string }).goal ?? "";
				} catch {
					/* the watch may be gone; forward with an empty goal rather than drop the event */
				}
				goals.set(watchId, goal);
				return goal;
			};
			const forward = async (e: Event & { watchId?: string }) => {
				const body = JSON.stringify(deliveryBody(e, await goalFor(e.watchId ?? "")));
				const started = ctx.now();
				let status: number | null = null;
				let error: string | undefined;
				try {
					const res = await ctx.fetch(target, {
						method: "POST",
						redirect: "manual",
						headers: { "content-type": "application/json", "percia-signature": await signWebhook(body, secret!, Math.floor(ctx.now() / 1000)), "user-agent": "percia-cli-listen" },
						body,
						signal: AbortSignal.timeout(10_000),
					});
					status = res.status;
				} catch (err) {
					error = (err as Error).message;
				}
				const result = { eventId: e.id, watchId: e.watchId, forwardedTo: target.origin + target.pathname, status, ms: ctx.now() - started, ...(error ? { error } : {}) };
				if (g.json) ndjson(ctx, result);
				else ctx.stdout(`${isoOrDash(e.at)}  ${e.watchId ?? ""}  ${e.type}  -> ${status ?? "no response"} (${result.ms} ms)${error ? `  ${stripControl(error)}` : ""}\n`);
			};

			const filters = { watchId: o.watch, limit: 100 };
			const initial = await client.events.list(filters);
			const initialSorted = [...initial.events].reverse();
			initialSorted.forEach((e) => seen.add(e.id));
			for (const e of o.replay > 0 ? initialSorted.slice(-o.replay) : []) await forward(e as never);

			const interval = Math.max(2, o.interval) * 1000;
			while (!ctx.signal.aborted) {
				await ctx.sleep(interval, ctx.signal).catch(() => {});
				if (ctx.signal.aborted) break;
				for (const e of await pollNew(() => client.events.list(filters), seen)) await forward(e as never);
			}
		});
}
export { json };
