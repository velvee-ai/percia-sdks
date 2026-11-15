import { existsSync, readFileSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { afterEach, beforeEach, describe, expect, it } from "vitest";
import { Env } from "./harness.js";

const contract = JSON.parse(readFileSync(new URL("../../spec/camera-push-contract.json", import.meta.url), "utf8"));
const created = contract.register.created;
const existing = contract.register.existing;
const TOKEN = created.body.token as string;
const ROTATED = contract.rotate.body.token as string;
const RTSP = "rtsp://admin:s3cret@192.168.1.20:554/stream1";

let e: Env;
beforeEach(() => {
	e = new Env();
	e.env.PERCIA_API_KEY = "pk_live_test";
});
afterEach(() => e.cleanup());

const store = () => join(e.env.PERCIA_CONFIG_DIR!, "push-cameras.json");
const mode = (p: string) => statSync(p).mode & 0o777;
const saved = () => JSON.parse(readFileSync(store(), "utf8")).cameras as Record<string, { token: string; cameraId: string }>;

describe("cameras push register", () => {
	it("prints the URL and the token once with a warning, saves it 0600", async () => {
		e.mock.script("createCamera", created);
		const r = await e.run("cameras", "push", "register", "--name", "Hall camera", "--external-id", "lan-cam-1");
		expect(r.code).toBe(0);
		expect(e.mock.requests[0]!.body).toEqual(contract.register.request);
		expect(r.out).toContain(created.body.whipUrl);
		expect(r.out.split(TOKEN).length - 1).toBe(1); // once
		expect(r.out).toMatch(/shown once/);
		expect(r.err).not.toContain(TOKEN);
		expect(mode(store())).toBe(0o600);
		expect(mode(dirname(store()))).toBe(0o700);
		expect(Object.values(saved())[0]!.token).toBe(TOKEN);
	});
	it("--no-save keeps nothing on disk", async () => {
		e.mock.script("createCamera", created);
		const r = await e.run("cameras", "push", "register", "--name", "n", "--external-id", "x", "--no-save");
		expect(existsSync(store())).toBe(false);
		expect(r.out).toContain("Not saved");
	});
	it("an existing camera shows no token and explains how to get one", async () => {
		e.mock.script("createCamera", existing);
		const r = await e.run("cameras", "push", "register", "--name", "n", "--external-id", "lan-cam-1");
		expect(r.code).toBe(0);
		expect(r.out).toContain("already existed");
		expect(r.out).toContain("percia cameras token rotate cam_push_1");
		expect(r.out).not.toContain("pc_");
	});
	it("--rtsp prints commands with the placeholder, never the token or the RTSP password in a log line we own", async () => {
		e.mock.script("createCamera", created);
		const r = await e.run("cameras", "push", "register", "--name", "n", "--external-id", "x", "--rtsp", RTSP);
		expect(r.out).toContain('-authorization "$PERCIA_CAMERA_TOKEN"');
		expect(r.out).toContain("whipclientsink");
		expect(r.out.split(TOKEN).length - 1).toBe(1);
	});
	it("--json includes the token once and the warning", async () => {
		e.mock.script("createCamera", created);
		const j = JSON.parse((await e.run("cameras", "push", "register", "--name", "n", "--external-id", "x", "--json")).out);
		expect(j).toMatchObject({ token: TOKEN, existing: false, whipUrl: created.body.whipUrl });
		expect(j.warning).toMatch(/once/);
	});
	it("typed API errors map to exit codes (camera_limit -> 5, bad external id -> 2)", async () => {
		const limit = { status: 429, body: { error: { code: "camera_limit", message: "at most 10" } } };
		e.mock.script("createCamera", limit, limit, limit); // the SDK retries 429 twice
		expect((await e.run("cameras", "push", "register", "--name", "n", "--external-id", "x")).code).toBe(5);
		e.mock.script("createCamera", { status: 400, body: { error: { code: "invalid_request", message: "bad", field: "externalId" } } });
		expect((await e.run("cameras", "push", "register", "--name", "n", "--external-id", "bad id")).code).toBe(2);
	});
});

describe("cameras token and status", () => {
	it("rotate prints the new token once and updates the saved copy; revoke drops it", async () => {
		e.mock.script("createCamera", created);
		await e.run("cameras", "push", "register", "--name", "n", "--external-id", "lan-cam-1");
		e.mock.script("rotateCameraToken", contract.rotate);
		const r = await e.run("cameras", "token", "rotate", "cam_push_1");
		expect(r.out.split(ROTATED).length - 1).toBe(1);
		expect(Object.values(saved())[0]!.token).toBe(ROTATED);
		const v = await e.run("cameras", "token", "revoke", "cam_push_1");
		expect(v.code).toBe(0);
		expect(Object.keys(saved())).toHaveLength(0);
		expect(e.mock.requests.map((x) => `${x.method} ${x.url.pathname}`).slice(-2)).toEqual(["POST /api/cameras/cam_push_1/token", "DELETE /api/cameras/cam_push_1/token"]);
	});
	it("rotating a phone camera is a clean conflict (exit 5)", async () => {
		e.mock.script("rotateCameraToken", { status: 409, body: { error: { code: "wrong_kind", message: "not a push camera" } } });
		const r = await e.run("cameras", "token", "rotate", "cam_phone");
		expect(r.code).toBe(5);
		expect(r.err).toContain("not a push camera");
	});
	it("status of one camera uses the status route and prints state and hint; --json is the server shape", async () => {
		e.mock.script("getCameraStatus", contract.status.online, contract.status.revoked);
		const r = await e.run("cameras", "status", "cam_push_1");
		expect(r.out).toMatch(/cam_push_1\s+push\s+online\s+online/);
		expect(r.out).toContain("Receiving video.");
		const j = JSON.parse((await e.run("cameras", "status", "cam_push_1", "--json")).out);
		expect(j).toMatchObject({ state: "revoked", hint: "The token was revoked. Rotate it to publish again." });
		expect(e.mock.requests.map((x) => x.url.pathname)).toEqual(["/api/cameras/cam_push_1/status", "/api/cameras/cam_push_1/status"]);
	});
	it("status without an id lists all cameras", async () => {
		e.mock.script("listCameras", { status: 200, body: [existing.body.camera] });
		expect((await e.run("cameras", "status")).out).toMatch(/cam_push_1\s+Hall camera\s+push\s+online/);
	});
	it("status on an older server (404 on the route) falls back to the list; unknown id exits 4", async () => {
		const notFound = { status: 404, body: { error: { code: "not_found", message: "Not found" } } };
		e.mock.script("getCameraStatus", notFound, notFound);
		e.mock.script("listCameras", { status: 200, body: [existing.body.camera] }, { status: 200, body: [] });
		expect(JSON.parse((await e.run("cameras", "status", "cam_push_1", "--json")).out)).toMatchObject({ derived: true, state: "online" });
		expect((await e.run("cameras", "status", "nope")).code).toBe(4);
	});
});

describe("cameras push run", () => {
	it("registers, runs ffmpeg -> WHIP with the token, heartbeats, hides the RTSP password", async () => {
		e.mock.script("createCamera", created);
		const r = await e.run("cameras", "push", "run", "--rtsp", RTSP, "--once");
		expect(r.code).toBe(0);
		const body = e.mock.requests[0]!.body as { externalId: string; name: string; kind: string };
		expect(body).toMatchObject({ kind: "push", name: "Camera 192.168.1.20" });
		expect(body.externalId).toMatch(/^cli-192\.168\.1\.20-[0-9a-f]{6}$/);
		expect(e.execs).toHaveLength(1);
		expect(e.execs[0]!.args).toEqual(["-hide_banner", "-loglevel", "warning", "-rtsp_transport", "tcp", "-i", RTSP, "-an", "-c:v", "copy", "-f", "whip", "-authorization", TOKEN, created.body.whipUrl]);
		expect(r.out + r.err).not.toContain(TOKEN);
		expect(r.out + r.err).not.toContain("s3cret");
		expect(r.err).toContain("rtsp://192.168.1.20:554/stream1");
		const beat = e.mock.requests.find((x) => x.operationId === "sendCameraHeartbeat")!;
		expect(beat.headers.get("authorization")).toBe(`Bearer ${TOKEN}`);
		expect(Object.values(saved())[0]!.token).toBe(TOKEN);
	});
	it("a rerun uses the saved token (idempotent register, no new token)", async () => {
		e.mock.script("createCamera", created, existing);
		await e.run("cameras", "push", "run", "--rtsp", RTSP, "--once");
		e.execs.length = 0;
		const r = await e.run("cameras", "push", "run", "--rtsp", RTSP, "--once");
		expect(r.code).toBe(0);
		expect(e.execs[0]!.args).toContain(TOKEN);
		expect(e.mock.requests.filter((x) => x.operationId === "rotateCameraToken")).toHaveLength(0);
	});
	it("existing camera without a saved token: explains, and --rotate fixes it", async () => {
		e.mock.script("createCamera", existing);
		const r = await e.run("cameras", "push", "run", "--rtsp", RTSP, "--once");
		expect(r.code).toBe(1);
		expect(r.err).toContain("--rotate");
		expect(e.execs).toHaveLength(0);
		e.mock.script("createCamera", existing);
		e.mock.script("rotateCameraToken", contract.rotate);
		expect((await e.run("cameras", "push", "run", "--rtsp", RTSP, "--once", "--rotate")).code).toBe(0);
		expect(e.execs[0]!.args).toContain(ROTATED);
	});
	it("explains a missing ffmpeg and a ffmpeg without the whip muxer, before touching the API", async () => {
		e.ffmpegMuxers = undefined;
		let r = await e.run("cameras", "push", "run", "--rtsp", RTSP);
		expect(r.code).toBe(1);
		expect(r.err).toMatch(/ffmpeg is not installed/);
		expect(r.err).toMatch(/7\.1/);
		e.ffmpegMuxers = " E mp4 MP4\n E webm WebM\n";
		r = await e.run("cameras", "push", "run", "--rtsp", RTSP);
		expect(r.err).toMatch(/no WHIP muxer/);
		expect(e.mock.requests).toHaveLength(0);
	});
	it("scrubs the token out of ffmpeg's output and hints at a rejected token", async () => {
		e.mock.script("createCamera", created);
		e.onExec = async (_c, _a, onStderr) => (onStderr(`WHIP request failed 401 Unauthorized for token ${TOKEN}\n`), { code: 1 });
		const r = await e.run("cameras", "push", "run", "--rtsp", RTSP, "--once");
		expect(r.code).toBe(1);
		expect(r.err).not.toContain(TOKEN);
		expect(r.err).toContain("[token]");
		expect(r.err).toContain("--rotate");
	});
	it("restarts ffmpeg when it exits, until Ctrl-C", async () => {
		e.mock.script("createCamera", created);
		let n = 0;
		e.onExec = async () => (++n >= 3 ? (e.ctl.abort(), { code: null }) : { code: 1 });
		const r = await e.run("cameras", "push", "run", "--rtsp", RTSP);
		expect(e.execs).toHaveLength(3);
		expect(r.err).toContain("Restarting");
		expect(r.code).toBe(0);
	});
	it("rejects a non-RTSP address and a bad mode", async () => {
		expect((await e.run("cameras", "push", "run", "--rtsp", "http://x/y")).code).toBe(2);
		expect((await e.run("cameras", "push", "run", "--rtsp", RTSP, "--mode", "fast")).code).toBe(2);
	});
	it("transcode mode re-encodes", async () => {
		e.mock.script("createCamera", created);
		await e.run("cameras", "push", "run", "--rtsp", RTSP, "--once", "--mode", "transcode");
		expect(e.execs[0]!.args).toContain("libx264");
	});
});
