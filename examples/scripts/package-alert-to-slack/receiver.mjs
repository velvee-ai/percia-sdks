// Receive signed Percia deliveries and forward them to a Slack incoming webhook.
//   PERCIA_WEBHOOK_SECRET=whsec_... SLACK_WEBHOOK_URL=https://hooks.slack.com/services/... node receiver.mjs
import { createServer } from "node:http";
import { SignatureError, verify } from "./verify.mjs";
import { formatSlackMessage } from "./slack.mjs";

export function createReceiver({ secret, forward, includeImage = false, now = () => Date.now() / 1000, seen = new Set() }) {
	return createServer(async (req, res) => {
		const send = (status, body) => { res.writeHead(status, { "content-type": "application/json" }); res.end(JSON.stringify(body)); };
		if (req.method !== "POST" || req.url !== "/hooks/percia") return send(404, { error: "not_found" });
		const chunks = [];
		let size = 0;
		for await (const c of req) { size += c.length; if (size > 256 * 1024) return send(413, { error: "too_large" }); chunks.push(c); }
		const raw = Buffer.concat(chunks);
		try { verify(raw, req.headers["percia-signature"], secret, now()); }
		catch (e) { if (e instanceof SignatureError) return send(401, { error: e.code }); throw e; }
		let event;
		try { event = JSON.parse(raw.toString("utf8")); } catch { return send(400, { error: "invalid_json" }); }
		if (typeof event?.id !== "string") return send(400, { error: "missing_id" });
		if (seen.has(event.id)) return send(200, { ok: true, duplicate: true });
		seen.add(event.id);
		send(200, { ok: true }); // acknowledge first
		try {
			await forward(formatSlackMessage(event, { includeImage }));
			console.log(`forwarded ${event.id} to Slack`); // never log imageUrl or the secret
		} catch (err) {
			seen.delete(event.id);
			console.error("slack forward failed:", err instanceof Error ? err.message : "error");
		}
	});
}

const postToSlack = (url) => async (message) => {
	const r = await fetch(url, { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify(message) });
	if (!r.ok) throw new Error(`Slack answered ${r.status}`);
};

if (import.meta.url === `file://${process.argv[1]}`) {
	const secret = process.env.PERCIA_WEBHOOK_SECRET;
	const slack = process.env.SLACK_WEBHOOK_URL;
	if (!secret || !slack) { console.error("Set PERCIA_WEBHOOK_SECRET and SLACK_WEBHOOK_URL."); process.exit(1); }
	const port = Number(process.env.PORT ?? 3000);
	createReceiver({ secret, forward: postToSlack(slack), includeImage: process.env.INCLUDE_IMAGE === "1" }).listen(port, () => console.log(`Listening on :${port}/hooks/percia`));
}
