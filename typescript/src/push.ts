// Camera push (cameras on a private network): the registration result and the helpers that turn it into publish commands.
// The publish token is a bearer secret shown ONCE. Nothing here logs it: command lines carry the placeholder
// `$PERCIA_CAMERA_TOKEN` unless you pass the token to `publishArgv`, which is for spawning a process, not for printing.
import type { Camera } from "./generated/types.gen.js";

/** The placeholder every printable command line uses for the publish token. Export it as an environment variable. */
export const TOKEN_PLACEHOLDER = "$PERCIA_CAMERA_TOKEN";
export const TOKEN_ENV = "PERCIA_CAMERA_TOKEN";

/**
 * Result of `cameras.registerPush`.
 *
 * - `existing: false`: the camera was just created and `token` is the publish token, shown once. Store it now.
 * - `existing: true`: a camera with this `externalId` already existed (HTTP 200). The server never returns a token twice,
 *   so `token` is `null` unless you asked `onExisting: "rotate"`, in which case it is a fresh token and the old one is dead.
 */
export type PushRegistration = {
	camera: Camera;
	/** `https://media.../cam/<uuid>/whip`: where a connector publishes WHIP. */
	whipUrl: string;
	/** `pc_...`, or `null` when this registration did not mint one (idempotent hit). */
	token: string | null;
	existing: boolean;
	/** True when `token` was minted by a rotate because `onExisting: "rotate"` was set. */
	rotated: boolean;
	/** Server-provided example commands (they carry the placeholder, never the token). */
	publish: Record<string, unknown> | undefined;
};

/** `JSON.stringify(reg)` and loggers see this: the token is replaced so a stray `console.log(reg)` is safe. */
export function redactRegistration<T extends { token?: string | null }>(reg: T): Omit<T, "token"> & { token: string | null } {
	return { ...reg, token: reg.token ? `${reg.token.slice(0, 3)}…[redacted]` : null };
}

/** Replace every occurrence of the token in a text (child process output, error messages). */
export function scrubToken(text: string, token: string | null | undefined): string {
	return token ? text.split(token).join("[token]") : text;
}

export type PublishOptions = {
	/** The camera's LAN address, e.g. `rtsp://user:pass@192.168.1.20/stream1`. Credentials in it are shown as given: it is the caller's own. */
	rtsp: string;
	/** `copy` (default) passes H.264 through; `transcode` re-encodes to 720p/10 fps/1.5 Mbit/s H.264 baseline for cameras that send H.265 or heavy streams. */
	mode?: "copy" | "transcode";
};

export type PublishCommands = {
	/** One shell line (token as `$PERCIA_CAMERA_TOKEN`). Needs an ffmpeg built with the `whip` muxer (ffmpeg 7.1 or newer). */
	ffmpeg: string;
	/** What to type into OBS (Settings > Stream, service "WHIP"). */
	obs: { service: "WHIP"; server: string; bearerToken: string; notes: string[] };
	/** `gst-launch-1.0` line using `whipclientsink` (gst-plugins-rs, webrtchttp). */
	gstreamer: string;
	/** Keep-alive every 20 s while publishing (online = seen in the last 60 s). */
	heartbeat: string;
	/** `export PERCIA_CAMERA_TOKEN=...` line template, never filled in. */
	env: string;
};

const quote = (s: string) => `'${s.replace(/'/g, `'\\''`)}'`;

const TRANSCODE_VF = `scale=-2:'min(ih,720)',fps=10,format=yuv420p`;

/** ffmpeg arguments (an argv, no shell) for `ffmpeg ... -f whip`. `token` goes in as an argument: pass it only to spawn. */
export function publishArgv(whipUrl: string, token: string, opts: PublishOptions): string[] {
	const input = ["-rtsp_transport", "tcp", "-i", opts.rtsp, "-an"];
	const video = opts.mode === "transcode"
		? ["-vf", TRANSCODE_VF, "-c:v", "libx264", "-profile:v", "baseline", "-preset", "veryfast", "-tune", "zerolatency", "-bf", "0", "-g", "20", "-b:v", "1500k", "-maxrate", "1500k", "-bufsize", "3000k"]
		: ["-c:v", "copy"];
	return [...(opts.mode === "transcode" ? ["-re"] : []), ...input, ...video, "-f", "whip", "-authorization", token, whipUrl];
}

/** Printable publish commands for a registration. The token never appears: they use `$PERCIA_CAMERA_TOKEN`. */
export function buildPublishCommands(reg: Pick<PushRegistration, "whipUrl">, opts: PublishOptions & { apiBase?: string }): PublishCommands {
	const argv = publishArgv(reg.whipUrl, TOKEN_PLACEHOLDER, opts).map((a, i, all) => (a === TOKEN_PLACEHOLDER && all[i - 1] === "-authorization" ? `"${TOKEN_PLACEHOLDER}"` : /^[\w@%+=:,./-]+$/.test(a) ? a : quote(a)));
	const api = (opts.apiBase ?? "https://playground.percia.ai").replace(/\/+$/, "").replace(/\/api$/, "");
	return {
		ffmpeg: ["ffmpeg", ...argv].join(" "),
		obs: {
			service: "WHIP",
			server: reg.whipUrl,
			bearerToken: TOKEN_PLACEHOLDER,
			notes: ["Output: x264, keyframe interval 2 s, B-frames 0, CBR 1500 kbit/s, no audio is fine.", "OBS 30.2 or newer has the WHIP service."],
		},
		gstreamer: `gst-launch-1.0 rtspsrc location=${quote(opts.rtsp)} protocols=tcp latency=200 ! rtph264depay ! h264parse ! whipclientsink signaller::whip-endpoint=${quote(reg.whipUrl)} signaller::auth-token="${TOKEN_PLACEHOLDER}"`,
		heartbeat: `curl -fsS -X POST -H "Authorization: Bearer ${TOKEN_PLACEHOLDER}" ${api}/api/cam/heartbeat`,
		env: `export ${TOKEN_ENV}=<the token from registration>`,
	};
}

export type BulkItem = { name: string; externalId: string };
export type BulkResult =
	| { externalId: string; ok: true; registration: PushRegistration }
	| { externalId: string; ok: false; error: unknown };

/**
 * `cameras.status(id)`: what `GET /cameras/{id}/status` returns. `state` is the one to act on: `waiting` (never seen),
 * `online`, `offline`, `revoked` (token revoked). `hint` names the likely reason and the next step.
 * `derived` is set (and `hint` is null, `revoked` never appears) only when an older server had no status route and the
 * SDK worked it out from the camera list; `name` and `externalId` are filled in the same case.
 */
export type CameraStatus = {
	id: string;
	kind: "phone" | "push" | "link" | "file";
	state: "waiting" | "online" | "offline" | "revoked";
	status: "online" | "offline" | "never";
	lastSeenAt: string | null;
	secondsSinceSeen: number | null;
	watchCount: number;
	hint: string | null;
	name?: string;
	externalId?: string | null;
	derived?: true;
};
