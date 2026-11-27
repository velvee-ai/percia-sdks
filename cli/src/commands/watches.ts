import { Command } from "commander";
import type { Context, GlobalOptions } from "../context.js";
import { CliError, EXIT } from "../errors.js";
import { isoOrDash, json, table } from "../output.js";
import { openSession } from "../session.js";

type Deps = { ctx: Context; globals: () => GlobalOptions };

export function registerWatches(program: Command, { ctx, globals }: Deps) {
	const w = program.command("watches").description("Manage watches.");

	w.command("list")
		.description("List your watches.")
		.action(async () => {
			const g = globals();
			const list = await (await openSession(ctx, g)).client.watches.list();
			if (g.json) return json(ctx, list);
			ctx.stdout(list.length ? table(list as Record<string, unknown>[], [{ key: "id" }, { key: "displayStatus", title: "status" }, { key: "goal", max: 50 }, { key: "sourceUrl", title: "source", max: 40 }, { key: "eventCount", title: "events" }]) : "No watches.\n");
		});

	w.command("get <id>")
		.description("Show one watch.")
		.action(async (id: string) => {
			const g = globals();
			const watch = await (await openSession(ctx, g)).client.watches.get(id);
			if (g.json) return json(ctx, watch);
			for (const [k, v] of Object.entries(watch)) if (v !== null && v !== undefined && typeof v !== "object") ctx.stdout(`${k.padEnd(14)} ${v}\n`);
		});

	w.command("create")
		.description("Create a watch. The webhook secret is printed once: save it.")
		.requiredOption("--source <url>", "camera: rtsp://, rtsps://, http(s):// video URL, or percia-cam://<cameraId>")
		.option("--goal <text>", "what to watch for, in plain words (5 to 500 characters)")
		.option("--agent <id>", "deploy a published agent instead of a goal")
		.option("--agent-version <n>", "pin an agent version", (v) => Number(v))
		.option("--webhook <url>", "send a signed webhook to this public https address")
		.option("--email <address>", "email this address (default: the account owner)")
		.action(async (o: { source: string; goal?: string; agent?: string; agentVersion?: number; webhook?: string; email?: string}) => {
			const g = globals();
			if (!o.goal && !o.agent) throw new CliError("Give --goal or --agent.", EXIT.USAGE);
			if (o.goal && o.agent) throw new CliError("Use --goal or --agent, not both.", EXIT.USAGE);
			if (o.webhook && o.email) throw new CliError("Use --webhook or --email, not both.", EXIT.USAGE);
			const body: Record<string, unknown> = { sourceUrl: o.source };
			if (o.goal) body.goal = o.goal;
			if (o.agent) Object.assign(body, { agentId: o.agent, ...(o.agentVersion ? { agentVersion: o.agentVersion } : {}) });
			if (o.webhook) body.notify = { type: "webhook", target: o.webhook };
			else if (o.email) body.notify = { type: "email", target: o.email };
			const created = (await (await openSession(ctx, g)).client.watches.create(body as never)) as { id?: string; webhookSecret?: string; [k: string]: unknown };
			if (g.json) return json(ctx, created);
			ctx.stdout(`Created watch ${created.id} (${created.displayStatus ?? "active"}).\n`);
			if (created.webhookSecret) ctx.stdout(`\nWebhook signing secret (shown only now, store it as PERCIA_WEBHOOK_SECRET):\n  ${created.webhookSecret}\n`);
		});

	for (const [name, status] of [["pause", "paused"], ["resume", "active"]] as const) {
		w.command(`${name} <id>`)
			.description(`${name === "pause" ? "Pause" : "Resume"} a watch.`)
			.action(async (id: string) => {
				const g = globals();
				const { client } = await openSession(ctx, g);
				const res = await (name === "pause" ? client.watches.pause(id) : client.watches.resume(id));
				if (g.json) return json(ctx, res);
				ctx.stdout(`Watch ${id} is now ${status}.\n`);
			});
	}

	w.command("delete <id>")
		.description("Delete a watch and its events. Needs the watches:delete scope.")
		.option("-y, --yes", "do not ask for confirmation")
		.action(async (id: string, o: { yes?: boolean }) => {
			const g = globals();
			if (!o.yes && !g.json && ctx.isTTY) {
				const answer = (await ctx.readSecret(`Delete watch ${id} and all its events? Type "delete" to confirm: `)).trim();
				if (answer !== "delete") throw new CliError("Not deleted.", EXIT.FAILURE);
			} else if (!o.yes && !ctx.isTTY) {
				throw new CliError("Refusing to delete without confirmation.", EXIT.USAGE, "Pass --yes.");
			}
			const res = await (await openSession(ctx, g)).client.watches.delete(id);
			if (g.json) return json(ctx, res);
			ctx.stdout(`Deleted watch ${id}.\n`);
		});

	w.command("test <id>")
		.description("Send a signed test delivery to the watch's webhook (no camera needed).")
		.action(async (id: string) => {
			const g = globals();
			const res = (await (await openSession(ctx, g)).client.watches.testDelivery(id)) as Record<string, unknown>;
			if (g.json) return json(ctx, res);
			ctx.stdout(`Test delivery: ${JSON.stringify(res)}\n`);
		});

	w.command("rotate-secret <id>")
		.description("Replace the webhook secret now (the old one stops verifying at once). Printed once.")
		.action(async (id: string) => {
			const g = globals();
			const res = (await (await openSession(ctx, g)).client.watches.rotateSecret(id)) as { webhookSecret?: string };
			if (g.json) return json(ctx, res);
			ctx.stdout(`New webhook signing secret (shown only now):\n  ${res.webhookSecret}\n`);
		});
}

export { isoOrDash };
