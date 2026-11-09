import { Command } from "commander";
import type { Context, GlobalOptions } from "../context.js";
import { CliError, EXIT } from "../errors.js";
import { isoOrDash, json, table } from "../output.js";
import { openSession } from "../session.js";

type Deps = { ctx: Context; globals: () => GlobalOptions };

export function registerHooks(program: Command, { ctx, globals }: Deps) {
	const h = program.command("hooks").description("REST hooks: signed deliveries of every event to an https address (needs the hooks:write scope).");
	h.command("list")
		.description("List hooks (addresses and secrets are never returned).")
		.action(async () => {
			const g = globals();
			const list = await (await openSession(ctx, g)).client.hooks.list();
			if (g.json) return json(ctx, list);
			ctx.stdout(list.length ? table(list.map((x) => ({ ...x, events: (x.events ?? []).join(","), lastDeliveredAt: isoOrDash(x.lastDeliveredAt) })) as Record<string, unknown>[], [{ key: "id" }, { key: "label" }, { key: "status" }, { key: "watchId", title: "watch" }, { key: "events" }, { key: "lastDeliveredAt", title: "last delivery" }, { key: "lastError", title: "error" }]) : "No hooks.\n");
		});
	h.command("create <url>")
		.description("Subscribe a public https address. The signing secret is printed once.")
		.option("--events <list>", "comma-separated: goal.met or *", "goal.met")
		.option("--watch <id>", "only events of this watch")
		.option("--label <text>", "a name to recognise it by")
		.action(async (url: string, o: { events: string; watch?: string; label?: string }) => {
			const g = globals();
			if (!/^https:\/\//.test(url)) throw new CliError("The hook address must be public https.", EXIT.USAGE, "To test against localhost use `percia listen --forward`.");
			const created = (await (await openSession(ctx, g)).client.hooks.create({ url, events: o.events.split(",").map((s) => s.trim()).filter(Boolean), ...(o.watch ? { watchId: o.watch } : {}), ...(o.label ? { label: o.label } : {}) } as never)) as { id?: string; secret?: string };
			if (g.json) return json(ctx, created);
			ctx.stdout(`Created hook ${created.id}.\n\nSigning secret (shown only now):\n  ${created.secret}\n`);
		});
	h.command("test <id>")
		.description("Send one signed goal.test event to the hook and show the receiver's answer.")
		.action(async (id: string) => {
			const g = globals();
			const res = await (await openSession(ctx, g)).client.hooks.test(id);
			if (g.json) return json(ctx, res);
			ctx.stdout(`${JSON.stringify(res)}\n`);
		});
	h.command("delete <id>")
		.description("Remove a hook (idempotent).")
		.action(async (id: string) => {
			const g = globals();
			const res = (await (await openSession(ctx, g)).client.hooks.delete(id)) as { deleted?: boolean };
			if (g.json) return json(ctx, res);
			ctx.stdout(res.deleted === false ? `Hook ${id} was already gone.\n` : `Deleted hook ${id}.\n`);
		});
}
