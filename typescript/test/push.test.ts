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
	it("status calls GET /cameras/:id/status and returns the server's state and hint", async () => {
		mock.script("getCameraStatus", contract.status.online);
		const st = await c().cameras.status("cam_push_1");
		expect(st).toMatchObject({ id: "cam_push_1", state: "online", status: "online", secondsSinceSeen: 12, watchCount: 1, hint: "Receiving video." });
		expect(st.derived).toBeUndefined();
		expect(mock.requests.map((r) => `${r.method} ${r.url.pathname}`)).toEqual(["GET /api/cameras/cam_push_1/status"]);
	});
	it("status passes revoked and waiting through", async () => {
		mock.script("getCameraStatus", contract.status.revoked, contract.status.waiting);
		expect((await c().cameras.status("cam_push_1")).state).toBe("revoked");
		expect(await c().cameras.status("cam_push_1")).toMatchObject({ state: "waiting", lastSeenAt: null, secondsSinceSeen: null });
	});
	it("status falls back to the list when the server has no status route (404), deriving the state", async () => {
		mock.script("getCameraStatus", { status: 404, body: { error: { code: "not_found", message: "Not found" } } });
		mock.script("listCameras", { status: 200, body: [existing.body.camera] });
		const st = await c().cameras.status("cam_push_1");
		expect(st).toMatchObject({ derived: true, state: "online", status: "online", kind: "push", watchCount: 1, hint: null, name: "Hall camera" });
		expect(mock.requests.map((r) => r.url.pathname)).toEqual(["/api/cameras/cam_push_1/status", "/api/cameras"]);
	});
	it("status: a camera that is on neither route is a NotFoundError (the original 404)", async () => {
		mock.script("getCameraStatus", { status: 404, body: { error: { code: "not_found", message: "No such camera" } } });
		mock.script("listCameras", { status: 200, body: [] });
		await expect(c().cameras.status("nope")).rejects.toBeInstanceOf(NotFoundError);
	});
	it("status: other errors (403) do not trigger the fallback", async () => {
		mock.script("getCameraStatus", { status: 403, body: { error: { code: "insufficient_scope", message: "needs cameras:read" } } });
		await expect(c().cameras.status("cam_push_1")).rejects.toMatchObject({ status: 403, code: "insufficient_scope" });
		expect(mock.requests).toHaveLength(1);
	});
	it("bulk sends one POST /cameras/bulk and maps every entry in order (token once, existing null)", async () => {
		mock.script("createCameras", contract.bulk.created);
		const res = await c().cameras.bulk(contract.bulk.request.cameras);
		expect(mock.requests).toHaveLength(1);
		expect(mock.requests[0]!.body).toEqual(contract.bulk.request);
		expect(res.map((r) => [r.externalId, r.ok])).toEqual([["a", true], ["b", true]]);
		const [a, b] = res as Extract<(typeof res)[number], { ok: true }>[];
		expect(a!.registration).toMatchObject({ existing: false, token: "pc_FAKE_TOKEN_bulk_a_0003" });
		expect(b!.registration).toMatchObject({ existing: true, token: null });
	});
	it("bulk: the 200 (every camera existed) is read like the 201", async () => {
		mock.script("createCameras", contract.bulk.allExisting);
		const res = await c().cameras.bulk(contract.bulk.request.cameras);
		expect(res.map((r) => r.ok && r.registration.existing && r.registration.token === null)).toEqual([true, true]);
	});
	it("bulk onExisting rotate mints a token only for the existing ones", async () => {
		mock.script("createCameras", contract.bulk.created);
		mock.script("rotateCameraToken", contract.rotate);
		const res = await c().cameras.bulk(contract.bulk.request.cameras, { onExisting: "rotate" });
		expect(res.map((r) => r.ok)).toEqual([true, true]);
		expect((res[1] as { registration: { token: string; rotated: boolean } }).registration).toMatchObject({ rotated: true, token: contract.rotate.body.token });
		expect(mock.requests.map((r) => `${r.method} ${r.url.pathname}`)).toEqual(["POST /api/cameras/bulk", "POST /api/cameras/cam_push_2/token"]);
	});
	it("bulk onExisting throw reports the existing item as failed and keeps the new one", async () => {
		mock.script("createCameras", contract.bulk.created);
		const res = await c().cameras.bulk(contract.bulk.request.cameras, { onExisting: "throw" });
		expect(res.map((r) => r.ok)).toEqual([true, false]);
	});
	it("bulk splits more than 10 items into chunks of 10", async () => {
		const items = Array.from({ length: 12 }, (_, i) => ({ name: `n${i}`, externalId: `id${i}` }));
		mock.handlers.set("createCameras", (rec) => {
			const cams = (rec.body as { cameras: { name: string; externalId: string }[] }).cameras;
			return { status: 201, body: { cameras: cams.map((x, i) => ({ camera: { id: `c_${x.externalId}`, name: x.name, kind: "push", externalId: x.externalId }, whipUrl: "https://m/whip", token: `pc_${i}` })) } };
		});
		const res = await c().cameras.bulk(items);
		expect(mock.requests.map((r) => (r.body as { cameras: unknown[] }).cameras.length)).toEqual([10, 2]);
		expect(res.every((r) => r.ok)).toBe(true);
		expect(res.map((r) => r.externalId)).toEqual(items.map((i) => i.externalId));
	});
	it("bulk: 429 camera_limit is all or nothing for the chunk and reported on every item", async () => {
		mock.script("createCameras", { status: 429, body: { error: { code: "camera_limit", message: "at most 10 cameras" } } });
		const res = await c().cameras.bulk(contract.bulk.request.cameras);
		expect(res.map((r) => r.ok)).toEqual([false, false]);
		expect(res.every((r) => !r.ok && (r.error as { code?: string }).code === "camera_limit")).toBe(true);
		expect(mock.requests).toHaveLength(1);
	});
	it("bulk falls back to one registerPush per item when the server has no bulk route (404), asking the bulk route once", async () => {
		mock.script("createCameras", { status: 404, body: { error: { code: "not_found", message: "Not found" } } });
		mock.handlers.set("createCamera", (rec) => {
			const b = rec.body as { externalId: string };
			return b.externalId === "bad" ? { status: 429, body: { error: { code: "camera_limit", message: "limit" } } } : { status: 201, body: { ...created.body, camera: { ...created.body.camera, externalId: b.externalId } } };
		});
		const res = await c().cameras.bulk([{ name: "a", externalId: "a" }, { name: "b", externalId: "bad" }, { name: "c", externalId: "c" }], { concurrency: 2 });
		expect(res.map((r) => [r.externalId, r.ok])).toEqual([["a", true], ["bad", false], ["c", true]]);
		expect(mock.requests.filter((r) => r.url.pathname === "/api/cameras/bulk")).toHaveLength(1);
		const failed = res[1]!;
		expect(!failed.ok && (failed.error as { code?: string }).code).toBe("camera_limit");
	});
	it("bulk: a 400 (duplicate externalIds) is reported on the items, not thrown", async () => {
		mock.script("createCameras", { status: 400, body: { error: { code: "invalid_request", message: "externalIds must be unique" } } });
		const res = await c().cameras.bulk([{ name: "a", externalId: "a" }, { name: "a2", externalId: "a" }]);
		expect(res.map((r) => r.ok)).toEqual([false, false]);
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
