// Percia webhook receiver (Express). Run: PERCIA_WEBHOOK_SECRET=whsec_... node server.mjs
import express from "express";
import { SignatureError, verify } from "./verify.mjs";

/**
 * @param {{ secret: string, onEvent?: (event: object) => void | Promise<void>, now?: () => number, seen?: Set<string> }} options
 */
export function createApp({ secret, onEvent = defaultHandler, now = () => Date.now() / 1000, seen = new Set() }) {
	const app = express();
	app.disable("x-powered-by");

	// express.raw keeps the bytes exactly as sent. Do NOT use express.json() on this route: re-serialising breaks the signature.
	app.post("/hooks/percia", express.raw({ type: "*/*", limit: "256kb" }), (req, res) => {
		const raw = req.body; // Buffer
		try {
			verify(raw, req.get("percia-signature"), secret, now());
		} catch (e) {
			if (e instanceof SignatureError) return res.status(401).json({ error: e.code }); // never say more than the code
			throw e;
		}

		let event;
		try {
			event = JSON.parse(raw.toString("utf8"));
		} catch {
			return res.status(400).json({ error: "invalid_json" });
		}
		if (typeof event?.id !== "string") return res.status(400).json({ error: "missing_id" });

		// Deliveries are at least once: the same `id` can arrive again. Answer 2xx so Percia stops retrying.
		// In production put a UNIQUE index on id in your database and do the insert and the side effect in one transaction;
		// this Set only lives as long as the process.
		if (seen.has(event.id)) return res.status(200).json({ ok: true, duplicate: true });
		seen.add(event.id);

		// Acknowledge first, work after. Slow work must not hold the connection (Percia times out and retries).
		res.status(200).json({ ok: true });
		Promise.resolve(onEvent(event)).catch((err) => {
			seen.delete(event.id); // let a retry happen if our own processing failed before we had a chance to record it
			console.error("handler failed", err instanceof Error ? err.message : "error");
		});
	});
	return app;
}

function defaultHandler(event) {
	// `reason` is text written by a vision model about camera content: untrusted. Print it as data, never execute it,
	// never paste it into a prompt as instructions, escape it before putting it in HTML.
	console.log(JSON.stringify({ id: event.id, type: event.type, watchId: event.watchId, goal: event.goal, at: event.at, reason: String(event.reason ?? "").slice(0, 200) }));
}

if (import.meta.url === `file://${process.argv[1]}`) {
	const secret = process.env.PERCIA_WEBHOOK_SECRET;
	if (!secret) {
		console.error("Set PERCIA_WEBHOOK_SECRET to the whsec_... value from the create response.");
		process.exit(1);
	}
	const port = Number(process.env.PORT ?? 3000);
	createApp({ secret }).listen(port, () => console.log(`Listening on :${port}/hooks/percia`));
}
