import { Command } from "commander";
import type { Context, GlobalOptions } from "../context.js";
import { isoOrDash, json, qr, table } from "../output.js";
import { openSession } from "../session.js";

type Deps = { ctx: Context; globals: () => GlobalOptions };

export function registerCameras(program: Command, { ctx, globals }: Deps) {
	const c = program.command("cameras").description("Phone and laptop cameras.");
	c.command("add <name>")
		.description("Create a phone camera and print its pairing link (and a QR code) for the phone that will be the camera.")
		.option("--no-qr", "do not draw the QR code")
		.action(async (name: string, o: { qr: boolean }) => {
			const g = globals();
			const res = (await (await openSession(ctx, g)).client.cameras.create(name)) as { camera?: { id?: string; name?: string }; pairUrl?: string; pairExpiresAt?: string };
			if (g.json) return json(ctx, res);
			ctx.stdout(`Camera ${res.camera?.id} "${name}" created.\n\nOpen this link on the phone that will be the camera (single use, valid until ${isoOrDash(res.pairExpiresAt)}):\n  ${res.pairUrl}\n`);
			if (o.qr && res.pairUrl) ctx.stdout("\n" + (await qr(res.pairUrl)));
			ctx.stdout(`\nKeep the app or page open on screen while it watches. Then: percia watches create --source percia-cam://${res.camera?.id} --goal "..."\nThe link is private until used.\n`);
		});
	c.command("list")
		.description("List cameras.")
		.action(async () => {
			const g = globals();
			const list = await (await openSession(ctx, g)).client.cameras.list();
			if (g.json) return json(ctx, list);
			ctx.stdout(list.length ? table(list.map((x) => ({ ...x, lastSeenAt: isoOrDash(x.lastSeenAt) })) as Record<string, unknown>[], [{ key: "id" }, { key: "name" }, { key: "status" }, { key: "lastSeenAt", title: "last seen" }, { key: "watchCount", title: "watches" }]) : "No cameras.\n");
		});
	c.command("pair <id>")
		.description("Print a fresh pairing link for an existing camera.")
		.action(async (id: string) => {
			const g = globals();
			const res = (await (await openSession(ctx, g)).client.cameras.pair(id)) as { pairUrl?: string; pairExpiresAt?: string };
			if (g.json) return json(ctx, res);
			ctx.stdout(`Pairing link (single use, until ${isoOrDash(res.pairExpiresAt)}):\n  ${res.pairUrl}\n\n${res.pairUrl ? await qr(res.pairUrl) : ""}`);
		});
	c.command("remove <id>")
		.description("Remove a camera (409 while active or paused watches use it).")
		.action(async (id: string) => {
			const g = globals();
			const res = await (await openSession(ctx, g)).client.cameras.delete(id);
			if (g.json) return json(ctx, res);
			ctx.stdout(`Removed camera ${id}.\n`);
		});
}
