import { Command } from "commander";
import type { Context, GlobalOptions } from "../context.js";
import { CliError, EXIT } from "../errors.js";
import { isoOrDash, json, qr, table } from "../output.js";
import { openSession } from "../session.js";

type Deps = { ctx: Context; globals: () => GlobalOptions };

export function registerDestinations(program: Command, { ctx, globals }: Deps) {
	const d = program.command("destinations").alias("integrations").description("Alert destinations (Slack, Discord, Telegram, Home Assistant, IFTTT, Teams, PagerDuty, webhook).");
	d.command("list")
		.description("List connected destinations.")
		.action(async () => {
			const g = globals();
			const list = await (await openSession(ctx, g)).client.integrations.list();
			if (g.json) return json(ctx, list);
			ctx.stdout(list.length ? table(list.map((x) => ({ ...x, lastDeliveredAt: isoOrDash(x.lastDeliveredAt) })) as Record<string, unknown>[], [{ key: "id" }, { key: "service" }, { key: "label" }, { key: "status" }, { key: "default" }, { key: "lastDeliveredAt", title: "last delivery" }, { key: "lastError", title: "error" }]) : "No destinations connected. Try: percia destinations connect slack\n");
		});
	d.command("services")
		.description("Which services this host can connect.")
		.action(async () => {
			const g = globals();
			const list = await (await openSession(ctx, g)).client.integrations.services();
			if (g.json) return json(ctx, list);
			ctx.stdout(table(list as Record<string, unknown>[], [{ key: "service" }, { key: "name" }, { key: "connectKind", title: "connect via" }, { key: "available" }]));
		});
	d.command("connect <service>")
		.description("Start a connection and print the link a person opens while signed in to Percia (single use, 15 minutes). The CLI cannot finish it for you.")
		.option("--default", "make it a default destination: attached to every new watch")
		.option("--no-qr", "do not draw the QR code")
		.action(async (service: string, o: { default?: boolean; qr: boolean }) => {
			const g = globals();
			const { client } = await openSession(ctx, g);
			const known = ((await client.integrations.services().catch(() => [])) as { service?: string; available?: boolean }[]).filter((s) => s.service);
			if (known.length && !known.some((s) => s.service === service)) throw new CliError(`Unknown service "${service}".`, EXIT.USAGE, `Available: ${known.map((s) => s.service).join(", ")}`);
			if (known.find((s) => s.service === service)?.available === false) throw new CliError(`${service} is not available on this host.`, EXIT.FAILURE);
			const res = (await client.integrations.connect({ service, ...(o.default ? { default: true } : {}) } as never)) as { connectUrl?: string; expiresAt?: string };
			if (g.json) return json(ctx, res);
			ctx.stdout(`Open this link in your browser, signed in to Percia, to connect ${service} (expires ${isoOrDash(res.expiresAt)}):\n  ${res.connectUrl}\n`);
			if (o.qr && res.connectUrl) ctx.stdout("\n" + (await qr(res.connectUrl)));
			ctx.stdout(`\nWhen you are done: percia destinations list\n`);
		});
	d.command("remove <id>")
		.description("Remove a destination. Needs the watches:delete scope.")
		.action(async (id: string) => {
			const g = globals();
			const res = await (await openSession(ctx, g)).client.integrations.delete(id);
			if (g.json) return json(ctx, res);
			ctx.stdout(`Removed destination ${id}.\n`);
		});
	d.command("attach <watchId> <connectionId>")
		.description("Send a watch's alerts to a connected destination (adds a rule, keeps existing ones).")
		.option("--on <events>", "event filter", "*")
		.action(async (watchId: string, connectionId: string, o: { on: string }) => {
			const g = globals();
			const { client } = await openSession(ctx, g);
			const current = (await client.integrations.watchRules(watchId)) as { rules?: { connectionId: string; on: string }[] } | { connectionId: string; on: string }[];
			const rules = (Array.isArray(current) ? current : current.rules ?? []).map((r) => ({ connectionId: r.connectionId, on: r.on }));
			if (!rules.some((r) => r.connectionId === connectionId)) rules.push({ connectionId, on: o.on });
			const res = await client.integrations.setWatchRules(watchId, { rules } as never);
			if (g.json) return json(ctx, res);
			ctx.stdout(`Watch ${watchId} now alerts ${rules.length} destination(s).\n`);
		});
}
