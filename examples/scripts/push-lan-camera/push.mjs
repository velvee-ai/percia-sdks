// Push an RTSP camera on your LAN to Percia. Run it on a machine that can reach the camera.
//   PERCIA_API_KEY=pk_live_... RTSP_URL=rtsp://user:pass@192.168.1.20/stream1 node push.mjs
// It registers the camera (idempotent: running it again reuses the same camera), keeps the one-time publish token in
// .percia-camera-token (mode 0600, never printed), then runs ffmpeg RTSP -> WHIP and a heartbeat until Ctrl-C.
// Needs ffmpeg 7.1+ with the whip muxer (check: ffmpeg -muxers | grep whip). The camera serves ONE RTSP session.
import { createHash } from "node:crypto";
import { chmodSync, existsSync, readFileSync, writeFileSync } from "node:fs";
import { spawn } from "node:child_process";
import { createClient, publishArgv, scrubToken } from "@percia/sdk";

const env = process.env;
const apiKey = env.PERCIA_API_KEY;
const rtspUrl = env.RTSP_URL;
if (!apiKey || !rtspUrl) {
	console.error("Set PERCIA_API_KEY (scope cameras:write) and RTSP_URL (the camera's LAN address).");
	process.exit(2);
}
const baseUrl = (env.PERCIA_BASE_URL ?? "https://playground.percia.ai").replace(/\/$/, "");
const rtsp = new URL(rtspUrl);
const hidden = new URL(rtsp);
hidden.username = hidden.password = "";
const externalId = env.EXTERNAL_ID ?? `example-${rtsp.hostname}-${createHash("sha256").update(hidden.toString()).digest("hex").slice(0, 6)}`;
const name = env.CAMERA_NAME ?? `Camera ${rtsp.hostname}`;
const tokenFile = env.TOKEN_FILE ?? ".percia-camera-token";
const ffmpeg = env.FFMPEG ?? "ffmpeg";
const mode = env.MODE === "transcode" ? "transcode" : "copy";

const percia = createClient({ apiKey, baseUrl });

// 1. Register. Idempotent by externalId: the first call returns the token, later calls return the camera and token null.
const reg = await percia.cameras.registerPush({ name, externalId });
let token = reg.token;
if (token) {
	writeFileSync(tokenFile, token + "\n", { mode: 0o600 });
	chmodSync(tokenFile, 0o600);
	console.error(`Registered camera ${reg.camera.id}. The publish token (shown once) was saved to ${tokenFile}.`);
} else if (existsSync(tokenFile)) {
	token = readFileSync(tokenFile, "utf8").trim();
	console.error(`Camera ${reg.camera.id} already registered; using the token in ${tokenFile}.`);
} else {
	console.error(`Camera ${reg.camera.id} exists but there is no saved token, and Percia shows it only once.\nMint a new one (it stops other publishers using the old one): ROTATE=1 node push.mjs`);
	if (env.ROTATE !== "1") process.exit(1);
	token = (await percia.cameras.rotateToken(reg.camera.id)).token;
	writeFileSync(tokenFile, token + "\n", { mode: 0o600 });
	chmodSync(tokenFile, 0o600);
}

// 2. Keep-alive: online means seen in the last 60 s.
const beat = () => fetch(`${baseUrl}/api/cam/heartbeat`, { method: "POST", headers: { authorization: `Bearer ${token}` } }).catch(() => {});
await beat();
const timer = setInterval(beat, 20_000);

// 3. Publish: ffmpeg pulls the camera once and pushes it to the WHIP URL. Restart with backoff if it drops.
const stop = new AbortController();
process.on("SIGINT", () => stop.abort());
process.on("SIGTERM", () => stop.abort());
let delay = 2000;
let code = 0;
while (!stop.signal.aborted) {
	console.error(`Pushing ${hidden.toString()} -> ${reg.whipUrl}`);
	code = await new Promise((resolve) => {
		const child = spawn(ffmpeg, ["-hide_banner", "-loglevel", "warning", ...publishArgv(reg.whipUrl, token, { rtsp: rtspUrl, mode })], { stdio: ["ignore", "ignore", "pipe"], signal: stop.signal });
		child.stderr.on("data", (d) => process.stderr.write(scrubToken(String(d), token)));
		child.on("error", (e) => { if (!stop.signal.aborted) console.error(`Cannot start ${ffmpeg}: ${e.message}. Install ffmpeg 7.1+ (with the whip muxer).`); resolve(1); });
		child.on("close", (c) => resolve(c ?? 0));
	});
	if (env.ONCE === "1" || stop.signal.aborted) break;
	console.error(`ffmpeg exited (${code}); restarting in ${delay / 1000}s`);
	await new Promise((r) => setTimeout(r, delay));
	delay = Math.min(delay * 2, 30_000);
}
clearInterval(timer);
process.exit(stop.signal.aborted ? 0 : code);
