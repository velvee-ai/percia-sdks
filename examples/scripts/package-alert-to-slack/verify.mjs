// Verify a Percia webhook. Zero dependencies. Contract: docs/integrators/webhooks.md.
//
//   Percia-Signature: t=<unix seconds>,v1=<hex HMAC-SHA256(secret, "<t>.<raw body>")>
//
// If you use the SDK instead: import { verifyWebhookSignature } from "@percia/sdk" does the same.
import { createHmac, timingSafeEqual } from "node:crypto";

export const TOLERANCE_S = 300;

export class SignatureError extends Error {
	/** @param {"malformed"|"stale_timestamp"|"mismatch"} code */
	constructor(code) {
		super(code);
		this.code = code;
	}
}

/**
 * Throws SignatureError unless `header` is a fresh, valid signature of `rawBody` (a Buffer or string of the RAW bytes).
 * @param {Buffer|string} rawBody
 * @param {string|undefined} header
 * @param {string} secret the whole whsec_... string
 * @param {number} [now] unix seconds, for tests
 */
export function verify(rawBody, header, secret, now = Date.now() / 1000) {
	let t = null;
	const candidates = [];
	for (const part of (header ?? "").split(",")) {
		const i = part.indexOf("=");
		if (i < 0) continue;
		const key = part.slice(0, i).trim();
		const value = part.slice(i + 1).trim();
		if (key === "t" && /^[0-9]{1,12}$/.test(value)) t = Number(value);
		else if (key === "v1" && value) candidates.push(value);
	}
	if (t === null || candidates.length === 0) throw new SignatureError("malformed");
	if (Math.abs(now - t) > TOLERANCE_S) throw new SignatureError("stale_timestamp");
	const body = Buffer.isBuffer(rawBody) ? rawBody : Buffer.from(rawBody, "utf8");
	const expected = createHmac("sha256", secret).update(`${t}.`).update(body).digest();
	const ok = candidates.some((c) => {
		const got = Buffer.from(c, "utf8");
		const want = Buffer.from(expected.toString("hex"), "utf8");
		return got.length === want.length && timingSafeEqual(got, want);
	});
	if (!ok) throw new SignatureError("mismatch");
}
