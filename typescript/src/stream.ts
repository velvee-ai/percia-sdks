// Developer event feed: GET /api/events/stream (Server-Sent Events). Contract: percia-cf docs/specs/platform/dev-feed.md.
// A development and test tool, not a delivery path: webhooks stay the production path. Uses fetch streaming (no EventSource), so it
// can send the Authorization header and runs on Node 20+, Deno, Bun and Workers.
import { PerciaApiError, PerciaConnectionError, errorFromResponse, parseRetryAfter } from "./errors.js";
import { backoffMs, defaultSleep } from "./retry.js";
import type { WebhookEvent } from "./webhooks.js";

/** The JSON of one stream message: the webhook body plus `eventId` (and `concernId` when a concern of a deployed agent fired). `imageUrl` is never sent. */
export type StreamedEvent = Omit<WebhookEvent, "imageUrl"> & { eventId: string; concernId?: string };

export type EventStreamOptions = {
	/** Only events of this watch. A watch that is not yours answers 404 before the stream opens. */
	watchId?: string;
	concernId?: string;
	/** Event type, e.g. `goal.met`. */
	type?: string;
	/** First send the latest N events (0 to 20), oldest first. Only on the first connection. Default 0: start at "now". */
	backlog?: number;
	/** Resume after this cursor (the `cursor` of an earlier item). Sent as `?since=` on the first connection, then `Last-Event-ID`. */
	since?: string | number;
	/** Stop the stream (the iterator then ends without an error). */
	signal?: AbortSignal;
	/** Give up (throw) after this many failed connections in a row. Default: never. A connection that opened resets the count. */
	maxReconnects?: number;
	baseDelayMs?: number;
	maxDelayMs?: number;
	/** Reconnect when no byte (not even a ping) arrives for this long. The server pings every 15 s. Default 45000; 0 disables. */
	idleTimeoutMs?: number;
	/** Skip an event whose `eventId` was already yielded (a reconnect may replay one). Default true. */
	dedupe?: boolean;
	random?: () => number;
	sleep?: (ms: number, signal?: AbortSignal | null) => Promise<void>;
};

export type StreamItem =
	/** The stream is live (`: connected`). `attempt` is 1 on the first connection. */
	| { kind: "open"; attempt: number }
	/** One event. `data` is the exact JSON string the server sent: sign and forward that string, not a re-serialisation. */
	| { kind: "event"; cursor: string; event: StreamedEvent; data: string }
	/** The cursor is older than the replay window (5000 events). Backfill with `GET /api/events` once. */
	| { kind: "resync"; reason: string; from?: string }
	/** The server closed the stream on purpose (`max_duration` every 10 minutes, `lease_lost`, `error`). The iterator reconnects by itself. */
	| { kind: "end"; reason: string }
	/** The connection failed or ended; the iterator waits `delayMs` and reconnects with the last cursor. */
	| { kind: "reconnect"; attempt: number; delayMs: number; reason: string; status?: number; code?: string; message?: string }
	| { kind: "ping" };

export type SseFrame =
	| { kind: "comment"; text: string }
	| { kind: "retry"; ms: number }
	| { kind: "message"; id?: string; event: string; data: string };

/** Parse an SSE byte stream (WHATWG rules: LF, CR or CRLF line ends, multi-line `data`, comments, `retry`, BOM). */
export async function* parseSse(body: ReadableStream<Uint8Array>): AsyncGenerator<SseFrame> {
	const reader = body.getReader();
	const decoder = new TextDecoder("utf-8");
	let buf = "";
	let first = true;
	let id: string | undefined;
	let event = "";
	let data: string[] = [];
	let skipLF = false;
	const field = (line: string): SseFrame | undefined => {
		if (line === "") {
			const out: SseFrame | undefined = data.length ? { kind: "message", id, event: event || "message", data: data.join("\n") } : undefined;
			id = undefined;
			event = "";
			data = [];
			return out;
		}
		if (line.startsWith(":")) return { kind: "comment", text: line.slice(1).trim() };
		const i = line.indexOf(":");
		const name = i === -1 ? line : line.slice(0, i);
		let value = i === -1 ? "" : line.slice(i + 1);
		if (value.startsWith(" ")) value = value.slice(1);
		if (name === "id") {
			if (!value.includes("\0")) id = value;
		} else if (name === "event") event = value;
		else if (name === "data") data.push(value);
		else if (name === "retry" && /^\d+$/.test(value)) return { kind: "retry", ms: Number(value) };
		return undefined;
	};
	try {
		for (;;) {
			const { value, done } = await reader.read();
			let text = done ? decoder.decode() : decoder.decode(value, { stream: true });
			if (first && text) {
				first = false;
				if (text.charCodeAt(0) === 0xfeff) text = text.slice(1);
			}
			for (let i = 0; i < text.length; i++) {
				const ch = text[i]!;
				if (skipLF) {
					skipLF = false;
					if (ch === "\n") continue;
				}
				if (ch === "\r" || ch === "\n") {
					skipLF = ch === "\r";
					const f = field(buf);
					buf = "";
					if (f) yield f;
				} else buf += ch;
			}
			if (done) return; // an unterminated last message is dropped, like a browser does
		}
	} finally {
		reader.cancel().catch(() => {});
	}
}

export type StreamDeps = {
	/** The API base (`https://host/api`). */
	baseUrl: string;
	fetch: typeof fetch;
	/** Headers for one connection: authorization and the client header. Called per attempt so a refreshed token is picked up. */
	headers: () => Promise<Record<string, string>>;
};

const DEFAULT_RETRY_MS = 3000;
const SEEN_MAX = 2000;

function buildUrl(baseUrl: string, o: EventStreamOptions, cursor: string | undefined, firstConnection: boolean): string {
	const q = new URLSearchParams();
	if (o.watchId) q.set("watchId", o.watchId);
	if (o.concernId) q.set("concernId", o.concernId);
	if (o.type) q.set("type", o.type);
	if (firstConnection && cursor === undefined && o.backlog) q.set("backlog", String(o.backlog));
	// The first connection carries a given cursor as `?since=`; every later one uses `Last-Event-ID`.
	if (firstConnection && cursor !== undefined) q.set("since", cursor);
	const s = q.toString();
	return `${baseUrl}/events/stream${s ? `?${s}` : ""}`;
}

/**
 * The reconnecting stream. Yields `open`, `event`, `resync`, `end`, `reconnect` and `ping` items; ends when `signal` aborts.
 * Throws a typed `PerciaApiError` for what retrying cannot fix: 401 (key), 403 (missing `events:read`), 404 (not your watch), 400 (bad filter).
 * Reconnects (honouring `Retry-After` and the server's `retry:`) after 429, 5xx, network errors, `end` and idle connections.
 */
export async function* streamEvents(deps: StreamDeps, o: EventStreamOptions = {}): AsyncGenerator<StreamItem, void, void> {
	const sleep = o.sleep ?? defaultSleep;
	const random = o.random ?? Math.random;
	const baseDelayMs = o.baseDelayMs ?? 500;
	const maxDelayMs = o.maxDelayMs ?? 30_000;
	const idleMs = o.idleTimeoutMs ?? 45_000;
	const maxReconnects = o.maxReconnects ?? Infinity;
	if (o.backlog !== undefined && !(Number.isInteger(o.backlog) && o.backlog >= 0 && o.backlog <= 20)) throw new RangeError("backlog must be an integer from 0 to 20");
	if (o.since !== undefined && !/^\d+$/.test(String(o.since))) throw new RangeError("since must be a non-negative integer cursor");

	let cursor = o.since === undefined ? undefined : String(o.since);
	let retryMs = DEFAULT_RETRY_MS;
	let failures = 0; // consecutive connections that did not open
	let attempt = 0;
	let first = true;
	const seen = new Set<string>();
	const outer = o.signal;

	const wait = async (ms: number) => {
		try {
			await sleep(ms, outer);
		} catch (e) {
			if (!outer?.aborted) throw e;
		}
	};

	while (!outer?.aborted) {
		attempt++;
		const conn = new AbortController();
		const onAbort = () => conn.abort();
		outer?.addEventListener("abort", onAbort, { once: true });
		let idle: ReturnType<typeof setTimeout> | undefined;
		let idled = false;
		const bump = () => {
			if (!idleMs) return;
			clearTimeout(idle);
			idle = setTimeout(() => ((idled = true), conn.abort()), idleMs);
		};
		let delay = retryMs;
		let reason = "closed";
		let status: number | undefined;
		let code: string | undefined;
		let message: string | undefined;
		let opened = false;
		let ended = false;
		try {
			const headers = { ...(await deps.headers()), accept: "text/event-stream", "cache-control": "no-cache" } as Record<string, string>;
			if (cursor !== undefined && !first) headers["last-event-id"] = cursor;
			bump();
			const res = await deps.fetch(buildUrl(deps.baseUrl, o, cursor, first), { method: "GET", headers, signal: conn.signal });
			if (!res.ok || !res.body) {
				const text = await res.text().catch(() => "");
				let body: unknown = text;
				try {
					body = text ? JSON.parse(text) : undefined;
				} catch {
					/* keep the text */
				}
				const err = errorFromResponse(res, body);
				if (res.status === 429 || res.status >= 500) {
					status = res.status;
					code = err.code;
					message = err.message;
					reason = res.status === 429 ? "rate_limited" : "server_error";
					const ra = parseRetryAfter(res.headers.get("retry-after"));
					failures++;
					delay = ra ?? backoffMs(failures, { baseDelayMs, maxDelayMs, random });
					if (failures > maxReconnects) throw err;
				} else throw err; // 400, 401, 403, 404: retrying cannot help
			} else {
				first = false;
				for await (const frame of parseSse(res.body)) {
					bump();
					if (frame.kind === "retry") retryMs = Math.min(Math.max(frame.ms, 250), 60_000), (delay = retryMs);
					else if (frame.kind === "comment") {
						if (frame.text === "connected") {
							opened = true;
							failures = 0;
							yield { kind: "open", attempt };
						} else if (frame.text === "ping") yield { kind: "ping" };
					} else if (frame.event === "end" || frame.event === "resync") {
						let body: { reason?: string; from?: unknown } = {};
						try {
							body = JSON.parse(frame.data);
						} catch {
							/* a body-less end */
						}
						if (frame.event === "end") {
							ended = true;
							reason = body.reason ?? "end";
							yield { kind: "end", reason };
						} else yield { kind: "resync", reason: body.reason ?? "cursor_too_old", from: body.from === undefined ? undefined : String(body.from) };
					} else {
						let ev: StreamedEvent;
						try {
							ev = JSON.parse(frame.data) as StreamedEvent;
						} catch {
							continue; // not JSON: not an event of this contract
						}
						if (frame.id !== undefined && /^\d+$/.test(frame.id)) cursor = frame.id;
						if (o.dedupe !== false && ev.eventId) {
							if (seen.has(ev.eventId)) continue;
							seen.add(ev.eventId);
							if (seen.size > SEEN_MAX) seen.delete(seen.values().next().value as string);
						}
						yield { kind: "event", cursor: frame.id ?? cursor ?? "", event: ev, data: frame.data };
					}
				}
				if (!ended) reason = idled ? "idle_timeout" : "closed";
				if (!opened && !idled) {
					failures++;
					delay = backoffMs(failures, { baseDelayMs, maxDelayMs, random });
					if (failures > maxReconnects) throw new PerciaConnectionError("The event stream closed before it opened.");
				}
				if (ended && (reason === "lease_lost" || reason === "error")) delay = Math.max(delay, retryMs);
			}
		} catch (e) {
			if (outer?.aborted) return;
			if (e instanceof PerciaApiError || e instanceof PerciaConnectionError || e instanceof RangeError) throw e;
			status = undefined;
			reason = idled ? "idle_timeout" : "network_error";
			message = e instanceof Error ? e.message : String(e);
			if (!idled) {
				failures++;
				delay = backoffMs(failures, { baseDelayMs, maxDelayMs, random });
				if (failures > maxReconnects) throw new PerciaConnectionError(`Could not reach Percia: ${message}`, { cause: e });
			}
		} finally {
			clearTimeout(idle);
			outer?.removeEventListener("abort", onAbort);
			conn.abort();
		}
		if (outer?.aborted) return;
		yield { kind: "reconnect", attempt: attempt + 1, delayMs: delay, reason, ...(status ? { status } : {}), ...(code ? { code } : {}), ...(message ? { message } : {}) };
		await wait(delay);
	}
}
