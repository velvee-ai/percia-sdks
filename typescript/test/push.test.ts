import { beforeEach, describe, expect, it } from "vitest";
import { readFileSync } from "node:fs";
import { ConflictError, NotFoundError, PerciaError, RateLimitError, TOKEN_PLACEHOLDER, buildPublishCommands, createClient, publishArgv, redactRegistration, scrubToken } from "../src/index.js";
import { MockPercia } from "./mock-server.js";

const contract = JSON.parse(readFileSync(new URL("../../spec/camera-push-contract.json", import.meta.url), "utf8"));
const mock = new MockPercia();
beforeEach(() => mock.reset());
const c = () => createClient({ apiKey: "pk_live_test", baseUrl: "https://percia.test", fetch: mock.handle as typeof fetch, sleep: async () => {}, random: () => 0.5, maxRetries: 0 });
const created = contract.register.created;
const existing = contract.register.existing;
const TOKEN = created.body.token as string;

describe("cameras.registerPush", () => {
	it("creates: sends kind push + externalId and returns the one-time token", async () => {
		mock.script("createCamera", created);
		const reg = await c().cameras.registerPush({ name: "Hall camera", externalId: "lan-cam-1" });
		expect(mock.requests[0]!.body).toEqual(contract.register.request);
		expect(reg).toMatchObject({ existing: false, rotated: false, token: TOKEN, whipUrl: created.body.whipUrl });
		expect(reg.camera.kind).toBe("push");
	});
	it("idempotent 200: existing true, token null, nothing else called", async () => {
		mock.script("createCamera", existing);
		const reg = await c().cameras.registerPush({ name: "Hall camera", externalId: "lan-cam-1" });
		expect(reg).toMatchObject({ existing: true, token: null, rotated: false });
		expect(mock.requests).toHaveLength(1);
	});
	it("onExisting rotate mints a new token", async () => {
		mock.script("createCamera", existing);
		mock.script("rotateCameraToken", contract.rotate);
		const reg = await c().cameras.registerPush({ name: "Hall camera", externalId: "lan-cam-1", onExisting: "rotate" });
		expect(reg).toMatchObject({ existing: true, rotated: true, token: contract.rotate.body.token });
		expect(mock.requests.map((r) => `${r.method} ${r.url.pathname}`)).toEqual(["POST /api/cameras", "POST /api/cameras/cam_push_1/token"]);
	});
	it("onExisting throw raises a PerciaError that names rotateToken", async () => {
		mock.script("createCamera", existing);
		const err = await c().cameras.registerPush({ name: "n", externalId: "lan-cam-1", onExisting: "throw" }).catch((e) => e);
		expect(err).toBeInstanceOf(PerciaError);
		expect(err.message).toContain("rotateToken");
		expect(err.message).not.toContain("pc_");
	});
	it("typed errors carry the code", async () => {
		mock.script("createCamera", { status: 429, body: { error: { code: "camera_limit", message: "at most 10 cameras" } } });
		const err = await c().cameras.registerPush({ name: "n", externalId: "x" }).catch((e) => e);
		expect(err).toBeInstanceOf(RateLimitError);
		expect(err.code).toBe("camera_limit");
	});
	it("refuses a server that ignores kind (no whipUrl)", async () => {
		mock.script("createCamera", { status: 201, body: { camera: { id: "c" }, pairUrl: "https://x" } });
		await expect(c().cameras.registerPush({ name: "n", externalId: "x" })).rejects.toThrow(/whipUrl/);
	});
});

describe("token routes, status, bulk", () => {
	it("rotate and revoke hit /cameras/:id/token; wrong_kind is a ConflictError with code", async () => {
		mock.script("rotateCameraToken", contract.rotate);
		expect((await c().cameras.rotateToken("cam_push_1")).token).toBe(contract.rotate.body.token);
		await c().cameras.revokeToken("cam_push_1");
		expect(mock.requests.map((r) => `${r.method} ${r.url.pathname}`)).toEqual(["POST /api/cameras/cam_push_1/token", "DELETE /api/cameras/cam_push_1/token"]);
		mock.script("revokeCameraToken", { status: 409, body: { error: { code: "wrong_kind", message: "not a push camera" } } });
		const err = await c().cameras.revokeToken("cam_phone").catch((e) => e);
		expect(err).toBeInstanceOf(ConflictError);
		expect(err.code).toBe("wrong_kind");
	});
	it("rotate needs watches:delete too", async () => {
		mock.keys.set("pk_live_limited", ["cameras:write"]);
		const limited = createClient({ apiKey: "pk_live_limited", baseUrl: "https://percia.test", fetch: mock.handle as typeof fetch });
		await expect(limited.cameras.rotateToken("cam_push_1")).rejects.toMatchObject({ status: 403, code: "insufficient_scope" });
	});
	it("status reads the list; unknown id is a NotFoundError", async () => {
		mock.script("listCameras", { status: 200, body: [existing.body.camera] }, { status: 200, body: [] });
		expect(await c().cameras.status("cam_push_1")).toMatchObject({ status: "online", kind: "push", watchCount: 1 });
		await expect(c().cameras.status("nope")).rejects.toBeInstanceOf(NotFoundError);
	});
	it("bulk registers each item, keeps order and reports failures without stopping", async () => {
		mock.handlers.set("createCamera", (rec) => {
			const b = rec.body as { externalId: string };
			return b.externalId === "bad" ? { status: 429, body: { error: { code: "camera_limit", message: "limit" } } } : { status: 201, body: { ...created.body, camera: { ...created.body.camera, externalId: b.externalId } } };
		});
		const res = await c().cameras.bulk([{ name: "a", externalId: "a" }, { name: "b", externalId: "bad" }, { name: "c", externalId: "c" }], { concurrency: 2 });
		expect(res.map((r) => [r.externalId, r.ok])).toEqual([["a", true], ["bad", false], ["c", true]]);
		const failed = res[1]!;
		expect(!failed.ok && (failed.error as { code?: string }).code).toBe("camera_limit");
	});
});

describe("publish helpers never leak the token", () => {
	const reg = { whipUrl: created.body.whipUrl };
	it("printable commands use the placeholder", () => {
		const cmds = buildPublishCommands(reg, { rtsp: "rtsp://u:p@192.168.1.20/s", apiBase: "https://percia.test/api" });
		const all = JSON.stringify(cmds);
		expect(all).not.toContain("pc_");
		expect(cmds.ffmpeg).toBe(`ffmpeg -rtsp_transport tcp -i rtsp://u:p@192.168.1.20/s -an -c:v copy -f whip -authorization "${TOKEN_PLACEHOLDER}" ${reg.whipUrl}`);
		expect(cmds.gstreamer).toContain("whipclientsink");
		expect(cmds.heartbeat).toBe(`curl -fsS -X POST -H "Authorization: Bearer ${TOKEN_PLACEHOLDER}" https://percia.test/api/cam/heartbeat`);
		expect(cmds.obs).toMatchObject({ service: "WHIP", server: reg.whipUrl, bearerToken: TOKEN_PLACEHOLDER });
	});
	it("transcode mode re-encodes", () => {
		expect(buildPublishCommands(reg, { rtsp: "rtsp://h/s", mode: "transcode" }).ffmpeg).toContain("libx264");
	});
	it("argv carries the token only for spawning", () => {
		const argv = publishArgv(reg.whipUrl, TOKEN, { rtsp: "rtsp://h/s" });
		expect(argv).toEqual(["-rtsp_transport", "tcp", "-i", "rtsp://h/s", "-an", "-c:v", "copy", "-f", "whip", "-authorization", TOKEN, reg.whipUrl]);
	});
	it("redact and scrub", () => {
		const r = redactRegistration({ token: TOKEN, whipUrl: "u" });
		expect(JSON.stringify(r)).not.toContain(TOKEN);
		expect(scrubToken(`failed ${TOKEN} twice ${TOKEN}`, TOKEN)).toBe("failed [token] twice [token]");
		expect(scrubToken("x", null)).toBe("x");
	});
});
