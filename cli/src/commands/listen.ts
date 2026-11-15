import { Command } from "commander";
import { signWebhook, type Event, type PerciaClient, type StreamedEvent } from "@percia/sdk";
import { randomBytes, randomUUID } from "node:crypto";
import { readFile } from "node:fs/promises";
import { resolve } from "node:path";
import type { Context, GlobalOptions } from "../context.js";
import { CliError, EXIT, stripControl } from "../errors.js";
import { isoOrDash, ndjson } from "../output.js";
import { openSession } from "../session.js";
import { SeenSet } from "./events.js";

type Deps = { ctx: Context; globals: () => GlobalOptions };

/** The webhook body (docs/integrators/webhooks.md) plus `eventId`, rebuilt from a row of the event feed and the watch's goal. Used for `--replay` and for the backfill after a `resync`. */
export function deliveryBody(e: Event & { watchId?: string }, goal: string) {
	return { id: e.decisionId ?? e.id, watchId: e.watchId, occurrenceId: e.occurrenceId, type: e.type, goal, reason: e.reason, confidence: e.confidence, at: e.at, eventId: e.id, ...(e.concernId ? { concernId: e.concernId } : {}) };
}

const isLoopback = (u: URL) => ["localhost", "127.0.0.1", "[::1]", "::1"].includes(u.hostname) || u.hostname.endsWith(".localhost");
const short = (id: string | undefined) => (id ? stripControl(id).slice(0, 12) : "-");

type Options = {
	forwardTo?: string;
	watch?: string;
	concern?: string;
	type?: string;
	secretEnv?: string;
	secretFile?: string;
	backlog: number;
	print?: boolean;
	replay?: string;
	allowRemote?: boolean;
};

/** One line for a failed forward. Never includes request headers or the signature. */
export function describeForwardError(err: unknown, target: URL): string {
	const cause = (err as { cause?: { code?: string } } | undefined)?.cause;
	const code = cause?.code ?? (err as { code?: string }).code;
	if (code === "ECONNREFUSED") return `connection refused: nothing is listening on ${target.host}. Start your server, then events arrive again.`;
	if (code === "ENOTFOUND") return `cannot resolve ${target.hostname}`;
	if ((err as Error).name === "TimeoutError" || (err as Error).name === "AbortError") return "timed out after 10 s";
	return stripControl((err as Error).message);
}

async function readSecret(ctx: Context, o: Options): Promise<{ secret: string; generated: boolean }> {
	if (o.secretEnv && o.secretFile) throw new CliError("Use --secret-env or --secret-file, not both.", EXIT.USAGE);
	if (o.secretEnv) {
		const v = ctx.env[o.secretEnv]?.trim();
		if (!v) throw new CliError(`The environment variable ${o.secretEnv} is empty or not set.`, EXIT.USAGE, "Set it to the watch's webhookSecret (whsec_...).");
		return { secret: v, generated: false };
	}
	if (o.secretFile) {
		let text: string;
		try {
			text = await readFile(resolve(ctx.cwd, o.secretFile), "utf8");
		} catch (e) {
			throw new CliError(`Cannot read --secret-file ${o.secretFile}: ${(e as NodeJS.ErrnoException).code ?? "error"}.`, EXIT.USAGE);
		}
		if (!text.trim()) throw new CliError(`--secret-file ${o.secretFile} is empty.`, EXIT.USAGE);
		return { secret: text.trim(), generated: false };
	}
	const fromEnv = ctx.env.PERCIA_WEBHOOK_SECRET?.trim();
	if (fromEnv) return { secret: fromEnv, generated: false };
	return { secret: `whsec_local_${randomBytes(16).toString("hex")}`, generated: true };
}

export function registerListen(program: Command, { ctx, globals }: Deps) {
	program
		.command("listen")
		.description(
			"Receive events without a public URL: follows GET /api/events/stream and POSTs each event, signed like a real webhook, to a local server. A development tool, not a delivery path (see docs/local-development.md).",
		)
		.option("--forward-to <url>", "POST each event here, e.g. http://localhost:3000/hook (alias: --forward)")
		.option("--forward <url>", "alias of --forward-to")
		.option("--watch <id>", "only events of this watch")
		.option("--concern <id>", "only events of this agent concern")
		.option("--type <type>", "only this event type, e.g. goal.met")
		.option("--secret-env <NAME>", "read the watch's webhook secret (whsec_...) from this environment variable. Default: PERCIA_WEBHOOK_SECRET, else a generated local secret is printed once")
		.option("--secret-file <path>", "read the webhook secret from a file (keeps it out of the process list and shell history)")
		.option("--backlog <n>", "first send the latest n events (0 to 20), so a test sees something at once", (v) => Number(v), 0)
		.option("--print", "print each event as one JSON line on stdout (pipe it to jq); status lines go to stderr")
		.option("--replay <eventId>", "forward or print one past event once and exit (looked up in the event feed)")
		.option("--allow-remote", "allow a --forward-to target that is not localhost")
		.action(async (o: Options & { forward?: string }) => {
			const g = globals();
			o.forwardTo ??= o.forward;
			if (!o.forwardTo && !o.print) throw new CliError("Nothing to do: pass --forward-to <url>, --print, or both.", EXIT.USAGE, "Example: percia listen --forward-to http://localhost:3000/hook");
			if (!Number.isInteger(o.backlog) || o.backlog < 0 || o.backlog > 20) throw new CliError("--backlog must be a whole number from 0 to 20.", EXIT.USAGE);
			let target: URL | undefined;
			if (o.forwardTo) {
				try {
					target = new URL(o.forwardTo);
				} catch {
					throw new CliError(`--forward-to is not a URL: ${o.forwardTo}`, EXIT.USAGE);
				}
				if (!/^https?:$/.test(target.protocol)) throw new CliError("--forward-to must be http(s).", EXIT.USAGE);
				if (!isLoopback(target) && !o.allowRemote) throw new CliError("--forward-to points away from this machine.", EXIT.USAGE, "Pass --allow-remote if that is intended. Event text will be sent there.");
			}
			const signing = target ? await readSecret(ctx, o) : undefined;
			const { client, baseUrl } = await openSession(ctx, g);

			// Status goes to stderr when stdout carries data (--print, --json); results go to stdout otherwise.
			const info = (line: string) => (g.quiet ? undefined : ctx.stderr(line + "\n"));
			const result = (line: string, record: Record<string, unknown>) => {
				if (o.print) return void ctx.stderr(line + "\n");
				if (g.json) return void ndjson(ctx, record);
				ctx.stdout(line + "\n");
			};
			info(`Following ${baseUrl}/api/events/stream${target ? ` and forwarding to ${target.origin}${target.pathname}` : ""}. Ctrl-C to stop.`);
			if (target && signing) {
				if (signing.generated) info(`No webhook secret given: signing with a generated local one. Use it in your receiver while testing:\n  ${signing.secret}`);
				else info("Signing with the webhook secret you provided.");
			}
			info("This stream is for development: it carries no secret and is not retried or guaranteed. Production deliveries are webhooks.\n");

			let count = 0;
			const forward = async (e: StreamedEvent, data: string, cursor?: string) => {
				count++;
				if (o.print) ctx.stdout(data + "\n");
				if (!target || !signing) return;
				const started = ctx.now();
				let status: number | null = null;
				let error: string | undefined;
				try {
					const res = await ctx.fetch(target, {
						method: "POST",
						redirect: "manual",
						headers: {
							"content-type": "application/json",
							"percia-signature": await signWebhook(data, signing.secret, Math.floor(ctx.now() / 1000)),
							"user-agent": "percia-cli-listen",
							"x-percia-event-id": e.eventId ?? "",
							"x-percia-delivery-id": randomUUID(),
						},
						body: data,
						signal: AbortSignal.timeout(10_000),
					});
					status = res.status;
					await res.body?.cancel().catch(() => {});
				} catch (err) {
					error = describeForwardError(err, target);
				}
				const ms = ctx.now() - started;
				const line = `${isoOrDash(e.at)}  ${stripControl(e.type)}  watch ${short(e.watchId)}  event ${short(e.eventId)}  -> ${status ?? "failed"} (${ms} ms)${error ? `  ${error}` : ""}`;
				result(line, { eventId: e.eventId, watchId: e.watchId, type: e.type, cursor, forwardedTo: target.origin + target.pathname, status, ms, ...(error ? { error } : {}) });
			};

			const goals = new Map<string, string>();
			const goalFor = async (watchId: string) => {
				if (goals.has(watchId)) return goals.get(watchId)!;
				let goal = "";
				try {
					goal = ((await client.watches.get(watchId)) as { goal?: string }).goal ?? "";
				} catch {
					/* the watch may be gone; keep the event with an empty goal */
				}
				goals.set(watchId, goal);
				return goal;
			};
			const fromFeed = async (e: Event & { watchId?: string }) => {
				const body = deliveryBody(e, await goalFor(e.watchId ?? "")) as unknown as StreamedEvent;
				await forward(body, JSON.stringify(body));
			};

			if (o.replay) {
				let n = 0;
				for await (const e of client.events.iterate({ watchId: o.watch, type: o.type, limit: 100 })) {
					if (e.id === o.replay) return void (await fromFeed(e as never));
					if (++n >= 1000) break;
				}
				throw new CliError(`Event ${o.replay} was not found in your latest ${n} events.`, EXIT.NOT_FOUND, "Check the id (the `id` of `percia events list`, or `eventId` in a webhook body).");
			}

			const seen = new SeenSet();
			let lastAt = new Date(ctx.now()).toISOString();
			const backfill = async (c: PerciaClient) => {
				// `resync`: the server could not resume from our cursor. Fetch what the feed has since the last event we saw, once.
				const page = await c.events.list({ watchId: o.watch, type: o.type, since: lastAt, limit: 100 });
				for (const e of [...page.events].reverse()) {
					if (seen.has(e.id)) continue;
					seen.add(e.id);
					await fromFeed(e as never);
				}
			};

			for await (const item of client.events.stream({ watchId: o.watch, concernId: o.concern, type: o.type, backlog: o.backlog || undefined, signal: ctx.signal })) {
				switch (item.kind) {
					case "open":
						info(item.attempt === 1 ? "Connected." : "Reconnected.");
						break;
					case "event":
						seen.add(item.event.eventId);
						lastAt = item.event.at ?? lastAt;
						await forward(item.event, item.data, item.cursor);
						break;
					case "resync":
						info("The server could not resume from the last event (too old). Fetching what you missed from the event feed.");
						await backfill(client).catch((err) => info(`Backfill failed: ${stripControl((err as Error).message)}`));
						break;
					case "end":
						info(item.reason === "max_duration" ? "The server ends a stream every 10 minutes. Reconnecting." : `The server ended the stream (${stripControl(item.reason)}).`);
						break;
					case "reconnect":
						if (item.reason === "max_duration" || item.reason === "closed") break; // already said (end) or routine
						info(
							item.status === 429
								? `Too many streams or connects (${stripControl(item.message ?? "429")}). Retrying in ${Math.ceil(item.delayMs / 1000)}s. Close another \`percia listen\` if you have one.`
								: `Connection lost (${item.status ?? stripControl(item.reason)}). Retrying in ${Math.ceil(item.delayMs / 1000)}s.`,
						);
						break;
					case "ping":
						break;
				}
			}
			info(`\nStopped. ${count} event${count === 1 ? "" : "s"}.`);
		});
}
