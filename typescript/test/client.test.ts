import { afterEach, beforeEach, describe, expect, it } from "vitest";
import { billingOf, describeBilling, type Interpretation } from "../src/index.js";
import { AuthenticationError, ConflictError, NotFoundError, PerciaApiError, PerciaConnectionError, PerciaError, PermissionError, RateLimitError, ServerError, ValidationError, createClient, normalizeBaseUrl, toArray } from "../src/index.js";
import { MockPercia } from "./mock-server.js";

const mock = new MockPercia();
beforeEach(() => mock.reset());
const noSleep = { sleep: async () => {}, random: () => 0.5 };
const make = (extra = {}) => createClient({ apiKey: "pk_live_test", baseUrl: "https://percia.test", fetch: mock.handle as typeof fetch, ...noSleep, ...extra });

describe("client basics", () => {
	it("normalizes the base URL to <origin>/api", () => {
		expect(normalizeBaseUrl("https://x.test")).toBe("https://x.test/api");
		expect(normalizeBaseUrl("https://x.test/")).toBe("https://x.test/api");
		expect(normalizeBaseUrl("https://x.test/api/")).toBe("https://x.test/api");
		expect(normalizeBaseUrl()).toBe("https://playground.percia.ai/api");
	});
	it("rejects both apiKey and oauthToken", () => {
		expect(() => createClient({ apiKey: "a", oauthToken: "b" })).toThrow(PerciaError);
	});
	it("sends the api key as a Bearer token and the client header", async () => {
		await make().watches.list();
		const r = mock.requests[0];
		expect(r.headers.get("authorization")).toBe("Bearer pk_live_test");
		expect(r.headers.get("x-percia-client")).toMatch(/^percia-sdk-js\//);
		expect(r.url.pathname).toBe("/api/watches/mine");
	});
	it("sends an oauth token, resolving a token function on every request", async () => {
		let n = 0;
		mock.keys.set("tok_1", ["watches:read"]);
		mock.keys.set("tok_2", ["watches:read"]);
		const c = createClient({ oauthToken: () => `tok_${++n}`, baseUrl: "https://percia.test", fetch: mock.handle as typeof fetch });
		await c.watches.list();
		await c.watches.list();
		expect(mock.requests.map((r) => r.headers.get("authorization"))).toEqual(["Bearer tok_1", "Bearer tok_2"]);
	});
	it("runs the quickstart flow: create -> test -> get -> events -> delete", async () => {
		const c = make();
		const w = await c.watches.create({ sourceUrl: "rtsp://cam.example.com/stream", goal: "A person is standing at the front door", notify: { type: "webhook", target: "https://example.com/hooks/percia" } });
		expect(w.id).toBeTruthy();
		await c.watches.testDelivery("w_abc");
		await c.watches.get("w_abc");
		const page = await c.watches.listEvents("w_abc", { limit: 20 });
		expect(Array.isArray(page.events)).toBe(true);
		await c.watches.delete("w_abc");
		expect(mock.requests.map((r) => r.operationId)).toEqual(["createWatch", "testWatchDelivery", "getWatch", "listWatchEvents", "deleteWatch"]);
		expect(mock.requests[0].body).toMatchObject({ goal: "A person is standing at the front door" });
		expect(mock.requests[3].url.search).toBe("?limit=20");
	});
	it("pause and resume patch status", async () => {
		const c = make();
		await c.watches.pause("w_1");
		await c.watches.resume("w_1");
		expect(mock.requests.map((r) => r.body)).toEqual([{ status: "paused" }, { status: "active" }]);
	});
	it("every spec operation is reachable through client.api", () => {
		const c = make();
		for (const id of mock.operationIds()) expect(typeof (c.api as any)[id], id).toBe("function");
	});
	it("hooks, cameras, integrations hit the documented routes", async () => {
		const c = make();
		await c.hooks.create({ url: "https://hooks.zapier.com/x", events: ["goal.met"] });
		await c.hooks.list();
		await c.hooks.test("hk_1");
		await c.hooks.delete("hk_1");
		await c.cameras.create("Hall phone");
		await c.integrations.connect({ service: "slack" } as never);
		expect(mock.requests.map((r) => `${r.method} ${r.url.pathname}`)).toEqual(["POST /api/hooks", "GET /api/hooks", "POST /api/hooks/hk_1/test", "DELETE /api/hooks/hk_1", "POST /api/cameras", "POST /api/integrations/connect"]);
	});
});

describe("typed errors", () => {
	it("maps 401, 403, 404, 400, 409, 429, 5xx and carries request_id, code, field", async () => {
		const c = make({ maxRetries: 0 });
		mock.keys.set("pk_readonly", ["watches:read"]);
		const ro = make({ apiKey: "pk_readonly", maxRetries: 0 });
		const bad = make({ apiKey: "nope", maxRetries: 0 });

		await expect(bad.watches.list()).rejects.toBeInstanceOf(AuthenticationError);
		const e403 = await ro.watches.create({ sourceUrl: "rtsp://x", goal: "A person at the door" } as never).catch((e) => e);
		expect(e403).toBeInstanceOf(PermissionError);
		expect(e403.code).toBe("insufficient_scope");
		expect(e403.requiredScope).toBe("watches:write");
		expect(e403.requestId).toMatch(/^req_mock_/);

		mock.script("getWatch", { status: 404, body: { error: { code: "not_found", message: "No such watch", request_id: "req_body" }, message: "No such watch" } });
		const e404 = await c.watches.get("zzz").catch((e) => e);
		expect(e404).toBeInstanceOf(NotFoundError);
		expect(e404.requestId).toBe("req_body");
		expect(e404.status).toBe(404);

		mock.script("createWatch", { status: 400, body: { error: { code: "invalid_request", message: "Describe what to watch for", field: "goal" }, message: "Describe what to watch for" } });
		const e400 = await c.watches.create({ sourceUrl: "rtsp://x", goal: "" } as never).catch((e) => e);
		expect(e400).toBeInstanceOf(ValidationError);
		expect(e400.field).toBe("goal");
		// request id falls back to the response header when the body has none
		expect(e400.requestId).toBe("req_scripted");

		mock.script("deleteCamera", { status: 409, body: { error: { code: "camera_in_use", message: "in use" }, message: "in use" } });
		expect(await c.cameras.delete("c1").catch((e) => e)).toBeInstanceOf(ConflictError);

		mock.script("listWatches", { status: 429, body: { error: { code: "plan_limit", message: "cap" }, message: "cap" }, headers: { "retry-after": "7" } });
		const e429 = await c.watches.list().catch((e) => e);
		expect(e429).toBeInstanceOf(RateLimitError);
		expect(e429.retryAfterSec).toBe(7);

		mock.script("listWatches", { status: 500, body: { error: { code: "internal", message: "boom" }, message: "boom" } });
		const e500 = await c.watches.list().catch((e) => e);
		expect(e500).toBeInstanceOf(ServerError);
		expect(e500).toBeInstanceOf(PerciaApiError);
	});
	it("a non-JSON error body still yields a typed error", async () => {
		const c = make({ maxRetries: 0, fetch: async () => new Response("<html>bad gateway</html>", { status: 502, headers: { "content-type": "text/html" } }) });
		const e = await c.watches.list().catch((x) => x);
		expect(e).toBeInstanceOf(ServerError);
		expect(e.status).toBe(502);
	});
});

describe("retries", () => {
	it("retries 429 honoring Retry-After and then succeeds", async () => {
		const sleeps: number[] = [];
		const c = make({ sleep: async (ms: number) => void sleeps.push(ms) });
		mock.script("listWatches", { status: 429, headers: { "retry-after": "2" } }, { status: 429, headers: { "retry-after": "1" } });
		await c.watches.list();
		expect(sleeps).toEqual([2000, 1000]);
		expect(mock.requests).toHaveLength(3);
	});
	it("retries 503 on GET with exponential full-jitter backoff", async () => {
		const sleeps: number[] = [];
		const c = make({ sleep: async (ms: number) => void sleeps.push(ms), random: () => 1, baseDelayMs: 100, maxDelayMs: 150, maxRetries: 3 });
		mock.script("listWatches", { status: 503 }, { status: 503 }, { status: 502 });
		await c.watches.list();
		expect(sleeps).toEqual([100, 150, 150]);
	});
	it("gives up after maxRetries and throws the last error", async () => {
		const c = make({ maxRetries: 2 });
		mock.script("listWatches", { status: 503 }, { status: 503 }, { status: 503 }, { status: 503 });
		await expect(c.watches.list()).rejects.toBeInstanceOf(ServerError);
		expect(mock.requests).toHaveLength(3);
	});
	it("does not retry a POST on 5xx (the create may have happened) but retries it on 429", async () => {
		const c = make();
		mock.script("createWatch", { status: 500 });
		await expect(c.watches.create({ sourceUrl: "rtsp://x", goal: "A person at the door" } as never)).rejects.toBeInstanceOf(ServerError);
		expect(mock.requests).toHaveLength(1);
		mock.reset();
		mock.script("createWatch", { status: 429, headers: { "retry-after": "0" } });
		await c.watches.create({ sourceUrl: "rtsp://x", goal: "A person at the door" } as never);
		expect(mock.requests).toHaveLength(2);
		expect(mock.requests[1].body).toMatchObject({ goal: "A person at the door" }); // body re-sent intact
	});
	it("retryNonIdempotent opts a POST into 5xx retries", async () => {
		const c = make({ retryNonIdempotent: true });
		mock.script("createWatch", { status: 503 });
		await c.watches.create({ sourceUrl: "rtsp://x", goal: "A person at the door" } as never);
		expect(mock.requests).toHaveLength(2);
	});
	it("never retries other 4xx", async () => {
		const c = make();
		await expect(make({ apiKey: "bad" }).watches.list()).rejects.toBeInstanceOf(AuthenticationError);
		expect(mock.requests).toHaveLength(1);
		void c;
	});
	it("does not wait for a Retry-After above maxRetryAfterMs; returns the 429", async () => {
		const c = make({ maxRetryAfterMs: 5000 });
		mock.script("listWatches", { status: 429, headers: { "retry-after": "3600" } });
		const e = await c.watches.list().catch((x) => x);
		expect(e).toBeInstanceOf(RateLimitError);
		expect(e.retryAfterSec).toBe(3600);
		expect(mock.requests).toHaveLength(1);
	});
	it("retries network errors on GET, wraps them in PerciaConnectionError when exhausted", async () => {
		let calls = 0;
		const c = createClient({ apiKey: "k", baseUrl: "https://percia.test", maxRetries: 2, ...noSleep, fetch: (async () => { calls++; throw new TypeError("fetch failed"); }) as typeof fetch });
		await expect(c.watches.list()).rejects.toBeInstanceOf(PerciaConnectionError);
		expect(calls).toBe(3);
	});
	it("a caller abort is not retried", async () => {
		const ctl = new AbortController();
		const c = make();
		ctl.abort(new Error("stop"));
		const r = await c.api.listWatches({ signal: ctl.signal });
		expect((r.error as unknown as Error).message).toBe("stop"); // client.api never throws; the abort reason comes back untouched
		expect(mock.requests).toHaveLength(0);
	});
	it("times out a hung request", async () => {
		const c = createClient({ apiKey: "k", baseUrl: "https://percia.test", maxRetries: 0, timeoutMs: 20, fetch: ((req: Request) => new Promise((_, rej) => req.signal.addEventListener("abort", () => rej(req.signal.reason)))) as typeof fetch });
		await expect(c.watches.list()).rejects.toMatchObject({ name: "PerciaTimeoutError" });
	});
});

describe("pagination", () => {
	const ev = (i: number) => ({ id: `evt_${i}`, watchId: "w_1", at: "2026-11-01T09:30:00.000Z", type: "goal.met" });
	function feed(total: number, pageSize: number) {
		mock.handlers.set("listAccountEvents", (rec) => {
			const start = Number(rec.url.searchParams.get("cursor") ?? 0);
			const events = Array.from({ length: Math.min(pageSize, total - start) }, (_, i) => ev(start + i));
			const next = start + pageSize;
			return { status: 200, body: { events, nextCursor: next < total ? String(next) : null } };
		});
	}
	it("iterates every event across pages, newest first order preserved", async () => {
		feed(7, 3);
		const all = await toArray(make().events.iterate({ limit: 3 }));
		expect(all.map((e) => e.id)).toEqual([0, 1, 2, 3, 4, 5, 6].map((i) => `evt_${i}`));
		expect(mock.requests.map((r) => r.url.searchParams.get("cursor"))).toEqual([null, "3", "6"]);
	});
	it("is lazy: breaking out stops fetching", async () => {
		feed(100, 10);
		for await (const _ of make().events.iterate({ limit: 10 })) break;
		expect(mock.requests).toHaveLength(1);
	});
	it("handles an empty feed and a final empty page", async () => {
		feed(0, 10);
		expect(await toArray(make().events.iterate())).toEqual([]);
		mock.reset();
		mock.handlers.set("listAccountEvents", (rec) => (rec.url.searchParams.get("cursor") ? { status: 200, body: { events: [], nextCursor: null } } : { status: 200, body: { events: [ev(1)], nextCursor: "c1" } }));
		expect(await toArray(make().events.iterate())).toHaveLength(1);
	});
	it("passes filters through and converts since", async () => {
		feed(1, 10);
		await toArray(make().events.iterate({ watchId: "w_1", type: "goal.met", since: new Date("2026-11-01T00:00:00Z"), limit: 5 }));
		const q = mock.requests[0].url.searchParams;
		expect([q.get("watchId"), q.get("type"), q.get("since"), q.get("limit")]).toEqual(["w_1", "goal.met", "2026-11-01T00:00:00.000Z", "5"]);
	});
	it("iterates a watch's events and stops on a repeated cursor", async () => {
		mock.handlers.set("listWatchEvents", () => ({ status: 200, body: { events: [ev(1)], nextCursor: "same" } }));
		const got = await toArray(make().watches.iterateEvents("w_1"), 10);
		expect(got.length).toBeLessThanOrEqual(2);
	});
	it("watches.iterate yields the list", async () => {
		mock.handlers.set("listWatches", () => ({ status: 200, body: [{ id: "a" }, { id: "b" }] }));
		expect((await toArray(make().watches.iterate())).map((w) => w.id)).toEqual(["a", "b"]);
	});
});

describe("over real HTTP", () => {
	let srv: { origin: string; close: () => Promise<void> };
	beforeEach(async () => (srv = await mock.listen()));
	afterEach(() => srv.close());
	it("works end to end with the global fetch", async () => {
		const c = createClient({ apiKey: "pk_live_test", baseUrl: srv.origin });
		const w = await c.watches.create({ sourceUrl: "rtsp://cam.example.com/s", goal: "A person at the door", notify: { type: "email", target: "a@b.co" } });
		expect(w.id).toBeTruthy();
		await expect(createClient({ apiKey: "bad", baseUrl: srv.origin }).watches.list()).rejects.toBeInstanceOf(AuthenticationError);
		mock.script("listWatches", { status: 429, headers: { "retry-after": "0" } });
		await c.watches.list();
	});
});

const PLAN = {
	plan: "free", label: "Free", billingEnforced: true, selling: true, enforced: false, paid: false, hasCard: false,
	freeMinutes: 10, freeMinutesLeft: 4, creditMinutes: 20, minutesUsedThisMonth: 6, freeMinutesResetsAt: "2026-12-01T00:00:00.000Z",
	canStartWatches: true, blockReason: null, howCharged: "Charged by the exact camera-minute ($0.50 per camera-hour).", limitsNote: "Minutes are the real limit.",
	nextStep: "Add a card for 50 more free minutes.", bonusAvailable: true, bonusMinutes: 50, payment: { state: "active", billingUrl: "https://percia.test/billing" },
};

describe("billing, interpretation and device kind (additive)", () => {
	it("account.billing() maps a plan to the whoami billing block and describeBilling prints it", async () => {
		mock.handlers.set("getPlan", () => ({ status: 200, body: PLAN }));
		const b = await make().account.billing();
		expect(b).toMatchObject({ planLabel: "Free", freeMinutesRemaining: 4, creditMinutes: 20, minutesUsedThisMonth: 6, canStartWatches: true, paymentState: "active", paid: false, hasCard: false, bonusAvailable: true, bonusMinutes: 50, billingUrl: "https://percia.test/billing", blockReason: null });
		const text = describeBilling(b).join("\n");
		expect(text).toContain("4 left this month");
		expect(text).toContain("Credit:        20 minutes");
		expect(text).toContain("Next step:");
	});
	it("billingOf tolerates an older plan with none of the new fields, and flags a blocked account", () => {
		const old = billingOf({ plan: "free", limits: {}, counts: {} } as never);
		expect(old).toMatchObject({ planLabel: null, freeMinutesRemaining: null, canStartWatches: true, bonusAvailable: false, nextStep: null });
		const blocked = billingOf({ ...PLAN, canStartWatches: false, blockReason: "needs_billing", payment: { state: "blocked" } } as never);
		expect(blocked.canStartWatches).toBe(false);
		expect(describeBilling(blocked).join("\n")).toContain("blocked (needs_billing)");
	});
	it("watches.create sends interpret:false and concerns untouched", async () => {
		const c = make();
		await c.watches.create({ sourceUrl: "rtsp://cam.example.com/s", goal: "A car pulls in", interpret: false, kind: "event", notify: { type: "email", target: "a@b.co" } });
		expect(mock.requests.at(-1)!.body).toMatchObject({ interpret: false, kind: "event" });
		await c.watches.create({ sourceUrl: "rtsp://cam.example.com/s", goal: "Front door", concerns: [{ text: "A person stands at the door", kind: "state", ignore: ["the cat"] }], notify: { type: "email", target: "a@b.co" } });
		expect((mock.requests.at(-1)!.body as { concerns: unknown[] }).concerns).toHaveLength(1);
	});
	it("watches.interpret and reinterpret call their routes; a watch carries interpretation", async () => {
		mock.handlers.set("interpretGoal", () => ({ status: 200, body: { cached: false, deferred: false, interpretation: { concerns: [{ text: "A car pulls in", kind: "event" }], gaps: [], needsLook: false } } }));
		const c = make();
		const r = (await c.watches.interpret("Tell me when a car pulls in")) as { interpretation: Interpretation };
		expect(r.interpretation.concerns?.[0]?.kind).toBe("event");
		expect(mock.requests.at(-1)!.body).toEqual({ goal: "Tell me when a car pulls in" });
		await c.watches.reinterpret("w_1");
		expect(mock.requests.at(-1)!.url.pathname).toBe("/api/watches/w_1/reinterpret");
	});
	it("cameras.create passes deviceKind only when given, and list keeps old cameras (deviceKind null) working", async () => {
		const c = make();
		await c.cameras.create("Hall");
		expect(mock.requests.at(-1)!.body).toEqual({ name: "Hall" });
		await c.cameras.create("Desk", { deviceKind: "computer" });
		expect(mock.requests.at(-1)!.body).toEqual({ name: "Desk", deviceKind: "computer" });
		mock.handlers.set("listCameras", () => ({ status: 200, body: [{ id: "c1", name: "Old", deviceKind: null }, { id: "c2", name: "Tab", deviceKind: "tablet" }] }));
		const kinds = (await c.cameras.list()).map((x) => x.deviceKind ?? null);
		expect(kinds).toEqual([null, "tablet"]);
	});
});
