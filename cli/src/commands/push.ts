import { createHash } from "node:crypto";
import type { Command } from "commander";
import { TOKEN_ENV, buildPublishCommands, publishArgv, scrubToken, type PushRegistration } from "@percia/sdk";
import type { Context, GlobalOptions } from "../context.js";
import { CliError, EXIT } from "../errors.js";
import { json } from "../output.js";
import { getSaved, putSaved, pushStorePath } from "../push-store.js";
import { openSession } from "../session.js";

type Deps = { ctx: Context; globals: () => GlobalOptions };

const HEARTBEAT_MS = 20_000;
const WARNING = "This token is shown once. It can publish video to this one camera and nothing else. Treat it like a password.";

/** `rtsp://user:pass@host/path` -> `rtsp://host/path`: what we may print. */
export const withoutCredentials = (rtsp: string): string => {
	try {
		const u = new URL(rtsp);
		u.username = "";
		u.password = "";
		return u.toString();
	} catch {
		return "(invalid URL)";
	}
};

function parseRtsp(rtsp: string): URL {
	let u: URL;
	try {
		u = new URL(rtsp);
	} catch {
		throw new CliError(`"${withoutCredentials(rtsp)}" is not a URL.`, EXIT.USAGE, "Use the camera's LAN address, e.g. rtsp://user:pass@192.168.1.20:554/stream1");
	}
	if (u.protocol !== "rtsp:" && u.protocol !== "rtsps:") throw new CliError("--rtsp must be an rtsp:// or rtsps:// URL.", EXIT.USAGE);
	return u;
}

/** A stable id for a camera this machine pushes, so running the command again reuses the same Percia camera. */
export function defaultExternalId(rtsp: URL): string {
	const clean = new URL(rtsp.toString());
	clean.username = "";
	clean.password = "";
	const host = rtsp.hostname.replace(/[^A-Za-z0-9._:-]/g, "-");
	return `cli-${host}-${createHash("sha256").update(clean.toString()).digest("hex").slice(0, 6)}`.slice(0, 100);
}

/** Whether ffmpeg is installed and has the `whip` muxer (ffmpeg 7.1 or newer, built with WebRTC support). */
export async function checkFfmpeg(ctx: Context): Promise<void> {
	const res = await ctx.capture("ffmpeg", ["-hide_banner", "-muxers"]);
	if (!res) throw new CliError("ffmpeg is not installed (or not on PATH).", EXIT.FAILURE, "Install it (macOS: brew install ffmpeg; Debian/Ubuntu: apt install ffmpeg; Windows: winget install ffmpeg), version 7.1 or newer, then run this again. Or print the commands for OBS/GStreamer with `percia cameras push register --rtsp ...`.");
	if (!/^\s*E\w*\s+whip\s/m.test(res.stdout)) throw new CliError("This ffmpeg has no WHIP muxer, so it cannot publish to Percia.", EXIT.FAILURE, "The whip muxer arrived in ffmpeg 7.1 and needs a build with WebRTC support. Check `ffmpeg -muxers | grep whip`; update ffmpeg (brew upgrade ffmpeg), use a recent static build, or publish with OBS or GStreamer (`percia cameras push register --rtsp ...` prints the settings).");
}

function printRegistration(ctx: Context, reg: PushRegistration, o: { saved: boolean; rtsp?: string; baseUrl: string; storePath: string }) {
	const out = ctx.stdout;
	out(`Camera ${reg.camera.id} "${reg.camera.name}" (push) ${reg.existing ? "already existed" : "created"}.\n\nWHIP URL (not secret):\n  ${reg.whipUrl}\n\n`);
	if (reg.token) {
		out(`Publish token:\n  ${reg.token}\n\n!! ${WARNING}\n`);
		out(o.saved ? `   A copy is saved in ${o.storePath} (mode 0600) so \`percia cameras push run\` can reuse it. Use --no-save to skip that.\n` : "   Not saved (--no-save): store it now, it cannot be shown again.\n");
	} else if (o.saved) {
		out(`No token this time: it was shown when the camera was first registered, and the API never shows it twice.\nIf you did not keep it, mint a new one (the old one stops working): percia cameras token rotate ${reg.camera.id}\n`);
	}
	if (o.rtsp) {
		const c = buildPublishCommands(reg, { rtsp: o.rtsp, apiBase: o.baseUrl });
		out(`\nPublish from the machine on the camera's LAN (set ${TOKEN_ENV} first; commands never contain the token):\n  ffmpeg:\n    ${c.ffmpeg}\n  GStreamer:\n    ${c.gstreamer}\n  OBS: Settings > Stream > Service "WHIP", Server ${c.obs.server}, Bearer Token = the token\n  Keep-alive every 20 s (optional, \`push run\` does it for you):\n    ${c.heartbeat}\n`);
	}
}

export function registerPushCommands(cameras: Command, { ctx, globals }: Deps) {
	const push = cameras.command("push").description("Cameras on a private network: a machine on the camera's LAN pulls it once and pushes it to Percia (WHIP).");

	push
		.command("register")
		.description("Register (idempotently, by --external-id) a push camera. Prints the WHIP URL and, the first time only, the publish token.")
		.requiredOption("--name <name>", "camera name (1-60 characters)")
		.requiredOption("--external-id <id>", "your stable id for this camera (A-Za-z0-9._:- up to 100); registering it again returns the same camera")
		.option("--rtsp <url>", "also print publish commands for this camera's LAN address")
		.option("--rotate", "if the camera already exists, mint a new token (the old one stops working)")
		.option("--no-save", "do not keep the token in the config directory")
		.action(async (o: { name: string; externalId: string; rtsp?: string; rotate?: boolean; save: boolean }) => {
			const g = globals();
			const s = await openSession(ctx, g);
			const reg = await s.client.cameras.registerPush({ name: o.name, externalId: o.externalId, onExisting: o.rotate ? "rotate" : "return" });
			if (reg.token && o.save) await putSaved(ctx, s.baseUrl, { cameraId: reg.camera.id!, name: o.name, externalId: o.externalId, whipUrl: reg.whipUrl, token: reg.token, savedAt: new Date(ctx.now()).toISOString() });
			const had = o.save && !reg.token ? await getSaved(ctx, s.baseUrl, o.externalId) : undefined;
			if (g.json) return json(ctx, { camera: reg.camera, whipUrl: reg.whipUrl, token: reg.token, existing: reg.existing, rotated: reg.rotated, saved: Boolean(reg.token && o.save) || Boolean(had), warning: reg.token ? WARNING : undefined });
			printRegistration(ctx, reg, { saved: o.save, rtsp: o.rtsp, baseUrl: s.baseUrl, storePath: pushStorePath(ctx) });
			if (had) ctx.stdout(`A token for this camera is saved in ${pushStorePath(ctx)}: \`percia cameras push run --rtsp ...\` will use it.\n`);
		});

	push
		.command("run")
		.description("Quick start on a LAN machine: register the camera (idempotent), then run ffmpeg RTSP -> WHIP in the foreground until Ctrl-C. Needs ffmpeg 7.1+ with the whip muxer.")
		.requiredOption("--rtsp <url>", "the camera's LAN address, e.g. rtsp://user:pass@192.168.1.20/stream1")
		.option("--name <name>", "camera name (default: Camera <host>)")
		.option("--external-id <id>", "stable id (default: derived from the RTSP address, so a rerun reuses the camera)")
		.option("--mode <mode>", "copy (default, passes H.264 through) or transcode (720p, 10 fps, H.264 baseline: for H.265 or heavy streams)", "copy")
		.option("--rotate", "mint a new token if the camera exists and this machine has no saved token")
		.option("--once", "do not restart ffmpeg when it exits")
		.action(async (o: { rtsp: string; name?: string; externalId?: string; mode: string; rotate?: boolean; once?: boolean }) => {
			const g = globals();
			if (o.mode !== "copy" && o.mode !== "transcode") throw new CliError(`--mode must be copy or transcode, not "${o.mode}".`, EXIT.USAGE);
			const rtsp = parseRtsp(o.rtsp);
			const externalId = o.externalId ?? defaultExternalId(rtsp);
			const name = o.name ?? `Camera ${rtsp.hostname}`;
			await checkFfmpeg(ctx);
			const s = await openSession(ctx, g);
			const saved = await getSaved(ctx, s.baseUrl, externalId);
			const reg = await s.client.cameras.registerPush({ name, externalId, onExisting: o.rotate && !saved ? "rotate" : "return" });
			let token = reg.token ?? saved?.token ?? null;
			if (reg.token) await putSaved(ctx, s.baseUrl, { cameraId: reg.camera.id!, name, externalId, whipUrl: reg.whipUrl, token: reg.token, savedAt: new Date(ctx.now()).toISOString() });
			if (!token) throw new CliError(`Camera ${reg.camera.id} (${externalId}) already exists but this machine has no saved token for it, and the API shows a token only once.`, EXIT.FAILURE, `Run again with --rotate to mint a new one (it stops any other machine publishing with the old token), or: percia cameras token rotate ${reg.camera.id}`);
			const argv = publishArgv(reg.whipUrl, token, { rtsp: o.rtsp, mode: o.mode });
			const log = (t: string) => (g.quiet ? undefined : ctx.stderr(t));
			log(`${reg.existing ? "Using" : "Created"} camera ${reg.camera.id} "${reg.camera.name ?? name}". Pushing ${withoutCredentials(o.rtsp)} -> ${reg.whipUrl} (${o.mode}). Ctrl-C to stop.\n`);

			const stop = new AbortController();
			const onAbort = () => stop.abort();
			ctx.signal.addEventListener("abort", onAbort, { once: true });
			let warned = false;
			const beat = async () => {
				try {
					const r = await ctx.fetch(`${s.baseUrl}/api/cam/heartbeat`, { method: "POST", headers: { authorization: `Bearer ${token}` }, signal: stop.signal });
					if (r.status === 401 && !warned) (warned = true), log("Heartbeat refused: this camera's token was rotated or revoked. Run again with --rotate.\n");
				} catch {
					/* offline: ffmpeg's own errors will say so */
				}
			};
			await beat();
			const heart = (async () => {
				for (;;) {
					try {
						await ctx.sleep(HEARTBEAT_MS, stop.signal);
					} catch {
						return;
					}
					if (stop.signal.aborted) return;
					await beat();
				}
			})();

			let delay = 2_000;
			let code: number | null = 0;
			try {
				for (;;) {
					const tail: string[] = [];
					const started = ctx.now();
					const res = await ctx.exec("ffmpeg", ["-hide_banner", "-loglevel", "warning", ...argv], {
						signal: stop.signal,
						onStderr: (chunk) => {
							const text = scrubToken(chunk, token).trim();
							if (text) tail.push(...text.split(/\r?\n/).filter(Boolean));
							if (tail.length > 20) tail.splice(0, tail.length - 20);
						},
					});
					if (stop.signal.aborted) break;
					if (res.startError) throw new CliError(`Could not start ffmpeg: ${scrubToken(res.startError, token)}`, EXIT.FAILURE);
					code = res.code;
					const hint = tail.some((l) => /401|403|unauthori[sz]ed|forbidden/i.test(l)) ? "The token looks rejected: it may have been rotated or revoked. Run again with --rotate.\n" : "";
					if (code !== 0) ctx.stderr(`ffmpeg exited with code ${code}.\n${tail.length ? tail.map((l) => `  ${l}`).join("\n") + "\n" : ""}${hint}`);
					if (o.once) break;
					if (ctx.now() - started > 60_000) delay = 2_000;
					log(`Restarting in ${Math.round(delay / 1000)} s (Ctrl-C to stop).\n`);
					try {
						await ctx.sleep(delay, stop.signal);
					} catch {
						break;
					}
					delay = Math.min(delay * 2, 30_000);
				}
			} finally {
				stop.abort();
				ctx.signal.removeEventListener("abort", onAbort);
				await heart;
			}
			token = null;
			if (code && !ctx.signal.aborted) throw new CliError(`ffmpeg stopped with code ${code}.`, EXIT.FAILURE);
		});
}
