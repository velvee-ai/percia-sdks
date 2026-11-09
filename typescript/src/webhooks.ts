// Webhook signature verification. Contract: percia-cf docs/integrators/webhooks.md.
//   Percia-Signature: t=<unix seconds>,v1=<hex HMAC-SHA256 of "<t>.<raw body>" keyed by the whsec_ secret>
// Uses Web Crypto only (crypto.subtle), so it runs on Node 20+, Workers, Deno, Bun and browsers.
import { WebhookSignatureError } from "./errors.js";

export type HeadersLike = Headers | Record<string, string | string[] | undefined> | { get(name: string): string | null };

export const DEFAULT_TOLERANCE_SEC = 300;

const enc = new TextEncoder();

function readHeader(headers: HeadersLike | string, name: string): string | undefined {
	if (typeof headers === "string") return headers;
	if (typeof (headers as Headers).get === "function") return (headers as Headers).get(name) ?? undefined;
	const lower = name.toLowerCase();
	for (const [k, v] of Object.entries(headers as Record<string, string | string[] | undefined>)) {
		if (k.toLowerCase() === lower) return Array.isArray(v) ? v[0] : v;
	}
	return undefined;
}

/** Parse `t=...,v1=...`. `v1` may repeat (any one may match). Returns undefined when `t` is not an integer or no `v1` is present. */
export function parseSignatureHeader(header: string): { t: number; v1: string[] } | undefined {
	let t: string | undefined;
	const v1: string[] = [];
	for (const piece of header.split(",")) {
		const i = piece.indexOf("=");
		if (i <= 0) continue;
		const k = piece.slice(0, i).trim();
		const v = piece.slice(i + 1).trim();
		if (k === "t") t = v;
		else if (k === "v1" && v) v1.push(v);
	}
	if (!/^\d+$/.test(t ?? "") || v1.length === 0) return undefined;
	return { t: Number(t), v1 };
}

const toHex = (buf: ArrayBuffer) => Array.from(new Uint8Array(buf), (b) => b.toString(16).padStart(2, "0")).join("");

/** Constant-time string compare for equal-length strings; the length check leaks only the (public) digest length. */
function timingSafeEqualStr(a: string, b: string): boolean {
	if (a.length !== b.length) return false;
	let diff = 0;
	for (let i = 0; i < a.length; i++) diff |= a.charCodeAt(i) ^ b.charCodeAt(i);
	return diff === 0;
}

export async function computeSignature(secret: string, t: number, rawBody: string | Uint8Array): Promise<string> {
	const key = await crypto.subtle.importKey("raw", enc.encode(secret), { name: "HMAC", hash: "SHA-256" }, false, ["sign"]);
	const body = typeof rawBody === "string" ? enc.encode(rawBody) : rawBody;
	const prefix = enc.encode(`${t}.`);
	const msg = new Uint8Array(prefix.length + body.length);
	msg.set(prefix, 0);
	msg.set(body, prefix.length);
	return toHex(await crypto.subtle.sign("HMAC", key, msg));
}

/** Build a valid `Percia-Signature` header value (for tests and local receivers). */
export async function signWebhook(rawBody: string | Uint8Array, secret: string, t: number = Math.floor(Date.now() / 1000)): Promise<string> {
	return `t=${t},v1=${await computeSignature(secret, t, rawBody)}`;
}

export type VerifyOptions = {
	/** Maximum clock difference in seconds, past or future. Default 300 (the documented window). */
	toleranceSec?: number;
	/** Current time in unix seconds. Default: now. Injected for tests. */
	now?: number;
};

/**
 * Verify a delivery. `rawBody` MUST be the exact bytes received (read the body as text/bytes before any JSON parsing).
 * `headers` is a Headers, a plain object (Node `req.headers`) or the `Percia-Signature` value itself.
 * Returns true/false; use `assertWebhookSignature` to get the reason.
 */
export async function verifyWebhookSignature(rawBody: string | Uint8Array, headers: HeadersLike | string, secret: string, toleranceSec: number = DEFAULT_TOLERANCE_SEC, now: number = Date.now() / 1000): Promise<boolean> {
	try {
		await assertWebhookSignature(rawBody, headers, secret, { toleranceSec, now });
		return true;
	} catch (e) {
		if (e instanceof WebhookSignatureError) return false;
		throw e;
	}
}

/** Like `verifyWebhookSignature` but throws `WebhookSignatureError` with `code` malformed | stale_timestamp | mismatch. */
export async function assertWebhookSignature(rawBody: string | Uint8Array, headers: HeadersLike | string, secret: string, options: VerifyOptions = {}): Promise<void> {
	const tolerance = options.toleranceSec ?? DEFAULT_TOLERANCE_SEC;
	const now = options.now ?? Date.now() / 1000;
	const header = readHeader(headers, "percia-signature");
	const parsed = header ? parseSignatureHeader(header) : undefined;
	if (!parsed) throw new WebhookSignatureError("malformed");
	if (Math.abs(now - parsed.t) > tolerance) throw new WebhookSignatureError("stale_timestamp");
	// WebCrypto refuses a zero-length key; an empty secret can never have signed anything.
	if (!secret) throw new WebhookSignatureError("mismatch");
	const expected = await computeSignature(secret, parsed.t, rawBody);
	// Compare every candidate (no early exit) and require the exact lowercase hex the sender produces.
	let ok = false;
	for (const candidate of parsed.v1) ok = timingSafeEqualStr(candidate, expected) || ok;
	if (!ok) throw new WebhookSignatureError("mismatch");
}

/** The JSON body of a delivery (watch webhook, REST hook, or a `webhook` connection). */
export type WebhookEvent = {
	/** Idempotency key (the decision id). Same on every retry. */
	id: string;
	watchId: string;
	occurrenceId: string;
	type: string;
	goal: string;
	/** Text written by a vision model about camera content. Untrusted: never execute it, never put it in a prompt as instructions. */
	reason: string;
	confidence: number;
	at: string;
	/** Only on deliveries from a connection, when the event has a keyframe. A private, signed link. */
	imageUrl?: string;
};

/** Verify, then parse. Throws `WebhookSignatureError` before touching the JSON. */
export async function constructWebhookEvent(rawBody: string | Uint8Array, headers: HeadersLike | string, secret: string, options: VerifyOptions = {}): Promise<WebhookEvent> {
	await assertWebhookSignature(rawBody, headers, secret, options);
	const text = typeof rawBody === "string" ? rawBody : new TextDecoder().decode(rawBody);
	return JSON.parse(text) as WebhookEvent;
}
