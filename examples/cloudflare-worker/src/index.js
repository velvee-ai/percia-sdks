// Percia webhook receiver for Cloudflare Workers. Web Crypto only, no dependencies, so it also runs on Deno, Bun
// and Vercel/Netlify edge. Contract: docs/integrators/webhooks.md.

const TOLERANCE_S = 300;
const encoder = new TextEncoder();

const hexToBytes = (hex) => {
	if (hex.length % 2 !== 0 || !/^[0-9a-f]+$/.test(hex)) return null; // lowercase hex only, as the contract says
	const out = new Uint8Array(hex.length / 2);
	for (let i = 0; i < out.length; i++) out[i] = parseInt(hex.slice(i * 2, i * 2 + 2), 16);
	return out;
};

/**
 * @param {Uint8Array|string} rawBody the RAW bytes (use request.arrayBuffer(), never request.json())
 * @returns {Promise<{ ok: true } | { ok: false, code: "malformed"|"stale_timestamp"|"mismatch" }>}
 */
export async function verifySignature(rawBody, header, secret, nowSeconds = Date.now() / 1000) {
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
	if (t === null || candidates.length === 0) return { ok: false, code: "malformed" };
	if (Math.abs(nowSeconds - t) > TOLERANCE_S) return { ok: false, code: "stale_timestamp" };

	if (!secret) return { ok: false, code: "mismatch" }; // Web Crypto refuses a zero-length HMAC key
	const body = typeof rawBody === "string" ? encoder.encode(rawBody) : rawBody;
	const signed = new Uint8Array(encoder.encode(`${t}.`).length + body.length);
	signed.set(encoder.encode(`${t}.`));
	signed.set(body, encoder.encode(`${t}.`).length);
	const key = await crypto.subtle.importKey("raw", encoder.encode(secret), { name: "HMAC", hash: "SHA-256" }, false, ["verify"]);
	// subtle.verify compares in constant time; we never compare the MACs ourselves.
	for (const candidate of candidates) {
		const sig = hexToBytes(candidate);
		if (sig && sig.length === 32 && (await crypto.subtle.verify("HMAC", key, sig, signed))) return { ok: true };
	}
	return { ok: false, code: "mismatch" };
}

const json = (status, body) => new Response(JSON.stringify(body), { status, headers: { "content-type": "application/json" } });

export default {
	/** @param {Request} request @param {{ PERCIA_WEBHOOK_SECRET: string, SEEN?: KVNamespace }} env @param {ExecutionContext} ctx */
	async fetch(request, env, ctx, nowSeconds = Date.now() / 1000) {
		if (request.method !== "POST") return json(405, { error: "method_not_allowed" });
		if (!env.PERCIA_WEBHOOK_SECRET) return json(500, { error: "not_configured" });

		const raw = new Uint8Array(await request.arrayBuffer()); // raw bytes, before any parsing
		const result = await verifySignature(raw, request.headers.get("percia-signature"), env.PERCIA_WEBHOOK_SECRET, nowSeconds);
		if (!result.ok) return json(401, { error: result.code });

		let event;
		try {
			event = JSON.parse(new TextDecoder().decode(raw));
		} catch {
			return json(400, { error: "invalid_json" });
		}
		if (typeof event?.id !== "string") return json(400, { error: "missing_id" });

		// Dedupe on event.id (deliveries are at least once). KV is eventually consistent, so for strict exactly-once
		// use a D1 table with a UNIQUE index on id (INSERT ... ON CONFLICT DO NOTHING) or a Durable Object.
		if (env.SEEN) {
			if (await env.SEEN.get(event.id)) return json(200, { ok: true, duplicate: true });
			await env.SEEN.put(event.id, "1", { expirationTtl: 86400 });
		}

		// Do the slow work after answering: ctx.waitUntil keeps the Worker alive without holding the response.
		ctx?.waitUntil?.(handle(event));
		return json(200, { ok: true });
	},
};

async function handle(event) {
	// `event.reason` is untrusted model text about camera content. Log it as data; never run it, never use it as
	// prompt instructions, escape it before rendering.
	console.log(JSON.stringify({ id: event.id, type: event.type, watchId: event.watchId, goal: event.goal, at: event.at }));
}
