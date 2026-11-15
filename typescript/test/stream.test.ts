import { afterEach, beforeEach, describe, expect, it } from "vitest";
import { createHmac } from "node:crypto";
import { AuthenticationError, NotFoundError, PermissionError, RateLimitError, ServerError, createClient, parseSse, signWebhook, verifyWebhookSignature, type StreamItem } from "../src/index.js";
import { MockSse, end, evt, fail, hold, message, resync, send } from "./sse-server.js";

const mock = new MockSse();
let srv: { origin: string; close: () => Promise<void> };
beforeEach(async () => {
	mock.connections = [];
	mock.steps = [];
	srv = await mock.listen();
});
afterEach(() => srv.close());

const sleeps: number[] = [];
const client = (over: Record<string, unknown> = {}) => createClient({ apiKey: "pk_live_test", baseUrl: srv.origin, maxRetries: 0, random: () => 0.5, sleep: async (ms) => void sleeps.push(ms), ...over });
beforeEach(() => void (sleeps.length = 0));

/** Collect items until `n` events were seen (or the stream ends), then stop the stream. */
async function take(c: ReturnType<typeof client>, o: Parameters<ReturnType<typeof client>["events"]["stream"]>[0] = {}, events = 1): Promise<StreamItem[]> {
	const ctl = new AbortController();
	const items: StreamItem[] = [];
	for await (const it of c.events.stream({ ...o, signal: ctl.signal })) {
		items.push(it);
		if (items.filter((i) => i.kind === "event").length >= events) ctl.abort();
	}
	return items;
}

const bytes = (chunks: string[]) => new ReadableStream<Uint8Array>({ start(c) { for (const s of chunks) c.enqueue(new TextEncoder().encode(s)); c.close(); } });
const frames = async (chunks: string[]) => {
	const out = [];
	for await (const f of parseSse(bytes(chunks))) out.push(f);
	return out;
};

describe("SSE framing", () => {
	it("parses retry, comments, id/event/data and a message split across chunks", async () => {
		const out = await frames(["retry: 3000\n: connected\n\nid: 7\nev", "ent: goal.met\ndata: {\"a\":", "1}\n\n"]);
		expect(out).toEqual([{ kind: "retry", ms: 3000 }, { kind: "comment", text: "connected" }, { kind: "message", id: "7", event: "goal.met", data: '{"a":1}' }]);
	});
	it("handles CRLF and CR, multi-line data, a BOM, a lone CR then LF across chunks, and drops an unterminated message", async () => {
		const out = await frames(["﻿data: a\r\ndata: b\r\n\r\n", "data: c\r", "\n\r\ndata: d\n\ndata: unterminated"]);
		expect(out.map((f) => (f as { data: string }).data)).toEqual(["a\nb", "c", "d"]);
	});
	it("ignores unknown fields, an id with NUL and a non-numeric retry", async () => {
		const out = await frames(["foo: bar\nid: 1\u00002\nretry: soon\ndata: x\n\n"]);
		expect(out).toEqual([{ kind: "message", id: undefined, event: "message", data: "x" }]);
	});
});

describe("events.stream", () => {
	it("connects with the bearer key and Accept, yields open then events with the exact data string", async () => {
		const e = evt(5);
		mock.then(hold(message(e)));
		const items = await take(client(), { watchId: "w_abc", type: "goal.met", concernId: "c_1", backlog: 3 });
		expect(items.map((i) => i.kind)).toEqual(["open", "event"]);
		const ev = items[1] as Extract<StreamItem, { kind: "event" }>;
		expect(ev.cursor).toBe("5");
		expect(ev.data).toBe(JSON.stringify(e.body));
		expect(ev.event.eventId).toBe("evt-5");
		const c = mock.connections[0]!;
		expect(c.headers.authorization).toBe("Bearer pk_live_test");
		expect(c.headers.accept).toBe("text/event-stream");
		expect(c.headers["last-event-id"]).toBeUndefined();
		expect(Object.fromEntries(c.url.searchParams)).toEqual({ watchId: "w_abc", type: "goal.met", concernId: "c_1", backlog: "3" });
	});

	it("resumes after `end` with Last-Event-ID, no backlog, the server's retry delay, and dedupes a replayed event", async () => {
		mock.then(send(message(evt(5)), message(evt(6)), end("max_duration")), hold(message(evt(6)), message(evt(7))));
		const items = await take(client(), { backlog: 2 }, 3);
		const events = items.filter((i) => i.kind === "event").map((i) => (i as { cursor: string }).cursor);
		expect(events).toEqual(["5", "6", "7"]); // evt-6 sent twice, yielded once
		expect(items.find((i) => i.kind === "end")).toEqual({ kind: "end", reason: "max_duration" });
		expect(items.find((i) => i.kind === "reconnect")).toMatchObject({ reason: "max_duration", delayMs: 3000 });
		expect(mock.connections[1]!.headers["last-event-id"]).toBe("6");
		expect(mock.connections[1]!.url.searchParams.has("backlog")).toBe(false);
		expect(mock.connections[0]!.url.searchParams.get("backlog")).toBe("2");
		expect(sleeps).toEqual([3000]);
	});

	it("resumes after a dropped connection (no `end`) the same way", async () => {
		mock.then(send(message(evt(1))), hold(message(evt(2))));
		const items = await take(client(), {}, 2);
		expect(items.find((i) => i.kind === "reconnect")).toMatchObject({ reason: "closed" });
		expect(mock.connections[1]!.headers["last-event-id"]).toBe("1");
	});

	it("sends a given cursor as ?since on the first connection, then Last-Event-ID", async () => {
		mock.then(send(message(evt(9))), hold(message(evt(10))));
		await take(client(), { since: 8 }, 2);
		expect(mock.connections[0]!.url.searchParams.get("since")).toBe("8");
		expect(mock.connections[0]!.headers["last-event-id"]).toBeUndefined();
		expect(mock.connections[1]!.headers["last-event-id"]).toBe("9");
		expect(mock.connections[1]!.url.searchParams.has("since")).toBe(false);
	});

	it("yields resync and keeps going", async () => {
		mock.then(hold(resync(3), message(evt(100))));
		const items = await take(client(), { since: 3 });
		expect(items.find((i) => i.kind === "resync")).toEqual({ kind: "resync", reason: "cursor_too_old", from: "3" });
		expect(items.at(-1)).toMatchObject({ kind: "event", cursor: "100" });
	});

	it("yields ping for `: ping` comments", async () => {
		mock.then(hold(": ping\n\n", message(evt(1))));
		expect((await take(client())).map((i) => i.kind)).toEqual(["open", "ping", "event"]);
	});

	it("ends cleanly (no throw) when the signal aborts", async () => {
		mock.then(hold());
		const ctl = new AbortController();
		const seen: string[] = [];
		for await (const it of client().events.stream({ signal: ctl.signal })) {
			seen.push(it.kind);
			ctl.abort();
		}
		expect(seen).toEqual(["open"]);
	});

	it("rejects a bad backlog or cursor before connecting", async () => {
		await expect(client().events.stream({ backlog: 21 }).next()).rejects.toThrow(RangeError);
		await expect(client().events.stream({ since: "abc" }).next()).rejects.toThrow(RangeError);
		expect(mock.connections).toHaveLength(0);
	});
});

describe("errors and backoff", () => {
	it("throws a typed error for 401, 403 and 404 and does not retry", async () => {
		mock.then(fail(401, "invalid_api_key", "bad key"), fail(403, "insufficient_scope", "needs events:read"), fail(404, "not_found", "no such watch"));
		await expect(client().events.stream().next()).rejects.toBeInstanceOf(AuthenticationError);
		await expect(client().events.stream().next()).rejects.toBeInstanceOf(PermissionError);
		await expect(client().events.stream({ watchId: "w_x" }).next()).rejects.toBeInstanceOf(NotFoundError);
		expect(mock.connections).toHaveLength(3);
		expect(sleeps).toEqual([]);
	});

	it("429 waits Retry-After, announces it, then connects", async () => {
		mock.then(fail(429, "rate_limited", "At most 2 streams at once.", { "retry-after": "5" }), hold(message(evt(1))));
		const items = await take(client());
		expect(items[0]).toMatchObject({ kind: "reconnect", reason: "rate_limited", status: 429, delayMs: 5000, code: "rate_limited" });
		expect((items[0] as { message: string }).message).toContain("2 streams");
		expect(sleeps).toEqual([5000]);
	});

	it("5xx and a refused connection back off exponentially (full jitter) and reset after an open", async () => {
		mock.then(fail(503, "unavailable", "x"), fail(502, "bad_gateway", "x"), send(message(evt(1))), fail(503, "unavailable", "x"), hold(message(evt(2))));
		await take(client(), {}, 2);
		// random 0.5: attempt 1 -> 250, attempt 2 -> 500, closed stream after a successful open -> server retry 3000, then a fresh 250
		expect(sleeps).toEqual([250, 500, 3000, 250]);
	});

	it("maxReconnects turns endless retrying into an error", async () => {
		mock.then(fail(503, "unavailable", "x"), fail(503, "unavailable", "x"), fail(503, "unavailable", "x"));
		const run = async () => {
			for await (const _ of client().events.stream({ maxReconnects: 2 })) void _;
		};
		await expect(run()).rejects.toBeInstanceOf(ServerError);
		expect(mock.connections).toHaveLength(3);
	});

	it("a network error (nothing listening) is retried, not thrown", async () => {
		await srv.close();
		const ctl = new AbortController();
		const kinds: string[] = [];
		for await (const it of client().events.stream({ signal: ctl.signal })) {
			kinds.push(it.kind);
			if (kinds.length >= 2) ctl.abort();
		}
		expect(kinds).toEqual(["reconnect", "reconnect"]);
		srv = await mock.listen();
	});

	it("reconnects when the connection goes silent for longer than the idle timeout", async () => {
		mock.then((c) => void c.res.writeHead(200, { "content-type": "text/event-stream" }), hold(message(evt(1))));
		const items = await take(client(), { idleTimeoutMs: 50 });
		expect(items.find((i) => i.kind === "reconnect")).toMatchObject({ reason: "idle_timeout" });
		expect(items.at(-1)).toMatchObject({ kind: "event" });
	});
});

describe("signing what the stream carries", () => {
	const secret = "whsec_test_secret";
	it("signs the exact data string like a real webhook and verifies against the documented algorithm", async () => {
		mock.then(hold(message(evt(1, { reason: 'quotes "and" unicode é' }))));
		const [, ev] = (await take(client())) as [unknown, Extract<StreamItem, { kind: "event" }>];
		const t = 1_794_000_000;
		const header = await signWebhook(ev.data, secret, t);
		// The documented verification (docs/integrators/webhooks.md, Node snippet), written independently of the SDK.
		const documented = (raw: string, h: string, key: string, now: number) => {
			const parts = Object.fromEntries(h.split(",").map((p) => p.split("=", 2)));
			if (Math.abs(now - Number(parts.t)) > 300) return false;
			return createHmac("sha256", key).update(`${Number(parts.t)}.${raw}`).digest("hex") === parts.v1;
		};
		expect(header).toMatch(/^t=\d+,v1=[0-9a-f]{64}$/);
		expect(documented(ev.data, header, secret, t + 1)).toBe(true);
		expect(await verifyWebhookSignature(ev.data, header, secret, 300, t + 1)).toBe(true);
		// A re-serialised body, another secret or a stale timestamp must fail.
		expect(await verifyWebhookSignature(JSON.stringify(JSON.parse(ev.data), null, 1), header, secret, 300, t)).toBe(false);
		expect(await verifyWebhookSignature(ev.data, header, "whsec_other", 300, t)).toBe(false);
		expect(await verifyWebhookSignature(ev.data, header, secret, 300, t + 301)).toBe(false);
	});
});
