import { Command } from "commander";
import type { Context, GlobalOptions } from "../context.js";
import { CliError, EXIT } from "../errors.js";
import { isoOrDash, json, qr, table } from "../output.js";
import { openSession } from "../session.js";
import { registerPushCommands } from "./push.js";
import { dropSavedByCameraId, pushStorePath, updateSavedToken } from "../push-store.js";

type Deps = { ctx: Context; globals: () => GlobalOptions };

export function registerCameras(program: Command, { ctx, globals }: Deps) {
	const c = program.command("cameras").description("Phone and laptop cameras, and push cameras on a private network.");
	c.command("add <name>")
		.description("Create a phone camera and print its pairing link (and a QR code) for the phone that will be the camera.")
		.option("--no-qr", "do not draw the QR code")
		.option("--device-kind <kind>", "phone, tablet or computer (only changes the wording shown on the pairing page)")
		.action(async (name: string, o: { qr: boolean; deviceKind?: string }) => {
			const g = globals();
			if (o.deviceKind && !["phone", "tablet", "computer"].includes(o.deviceKind)) throw new CliError("--device-kind is phone, tablet or computer.", EXIT.USAGE);
			const res = (await (await openSession(ctx, g)).client.cameras.create(name, o.deviceKind ? { deviceKind: o.deviceKind as "phone" | "tablet" | "computer" } : {})) as { camera?: { id?: string; name?: string }; pairUrl?: string; pairExpiresAt?: string };
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
			ctx.stdout(list.length ? table(list.map((x) => ({ ...x, lastSeenAt: isoOrDash(x.lastSeenAt) })) as Record<string, unknown>[], [{ key: "id" }, { key: "name" }, { key: "kind" }, { key: "deviceKind", title: "device" }, { key: "externalId", title: "external id" }, { key: "status" }, { key: "lastSeenAt", title: "last seen" }, { key: "watchCount", title: "watches" }]) : "No cameras.\n");
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
			const sess = await openSession(ctx, g);
			const res = await sess.client.cameras.delete(id);
			await dropSavedByCameraId(ctx, sess.baseUrl, id);
			if (g.json) return json(ctx, res);
			ctx.stdout(`Removed camera ${id}.\n`);
		});
	registerPushCommands(c, { ctx, globals });
	const token = c.command("token").description("Publish tokens of push cameras.");
	token
		.command("rotate <id>")
		.description("Mint a new publish token for a push camera (the old one stops working at once). Shown once. Needs cameras:write and watches:delete.")
		.option("--no-save", "do not update the token saved by `cameras push`")
		.action(async (id: string, o: { save: boolean }) => {
			const g = globals();
			const s = await openSession(ctx, g);
			const res = await s.client.cameras.rotateToken(id);
			const updated = o.save && res.token ? await updateSavedToken(ctx, s.baseUrl, id, res.token, res.whipUrl) : false;
			if (g.json) return json(ctx, { ...res, savedLocally: updated });
			ctx.stdout(`New publish token for camera ${id}:\n  ${res.token}\n\n!! This token is shown once. It can publish video to this one camera and nothing else. The old token no longer works.\n${updated ? `   Updated the saved copy in ${pushStorePath(ctx)}.\n` : ""}`);
		});
	token
		.command("revoke <id>")
		.description("Revoke a push camera's token: publishing stops at once, the camera stays. Rotate to publish again.")
		.action(async (id: string) => {
			const g = globals();
			const s = await openSession(ctx, g);
			const res = await s.client.cameras.revokeToken(id);
			const dropped = await dropSavedByCameraId(ctx, s.baseUrl, id);
			if (g.json) return json(ctx, { revoked: true, id, savedCopiesRemoved: dropped, response: res ?? null });
			ctx.stdout(`Revoked the publish token of camera ${id}. Publishing is refused until you run: percia cameras token rotate ${id}\n${dropped ? "Removed the saved copy.\n" : ""}`);
		});
	c.command("status [id]")
		.description("Show whether push cameras are online (seen in the last 60 s). One camera by id (state and what to do next), or all.")
		.action(async (id?: string) => {
			const g = globals();
			const client = (await openSession(ctx, g)).client;
			if (id) {
				const st = await client.cameras.status(id);
				if (g.json) return json(ctx, st);
				ctx.stdout(table([{ ...st, lastSeenAt: isoOrDash(st.lastSeenAt), secondsSinceSeen: st.secondsSinceSeen ?? "-" }] as Record<string, unknown>[], [{ key: "id" }, { key: "kind" }, { key: "state" }, { key: "status" }, { key: "lastSeenAt", title: "last seen" }, { key: "secondsSinceSeen", title: "seconds ago" }, { key: "watchCount", title: "watches" }]));
				if (st.hint) ctx.stdout(`${st.hint}\n`);
				return;
			}
			const list = await client.cameras.list();
			if (g.json) return json(ctx, list);
			ctx.stdout(list.length ? table(list.map((x) => ({ ...x, lastSeenAt: isoOrDash(x.lastSeenAt) })) as Record<string, unknown>[], [{ key: "id" }, { key: "name" }, { key: "kind" }, { key: "status" }, { key: "lastSeenAt", title: "last seen" }, { key: "watchCount", title: "watches" }]) : "No cameras.\n");
		});
}
