import { test } from "node:test";
import assert from "node:assert/strict";
import { createServer } from "node:http";
import { createHmac } from "node:crypto";
import { createClient } from "@percia/sdk";
import { forwardStream } from "../forward.mjs";

const SECRET = "whsec_example_secret";
const body = { id: "dec_1", watchId: "w_1", occurrenceId: "occ_1", type: "goal.met", goal: "g", reason: "r", confidence: 0.9, at: "2026-11-14T09:30:00Z", eventId: "6f1c2a52-0d9e-5b43-9a1e-2f7d6c1b8e40" };

const listen = (handler) => new Promise((r) => { const s = createServer(handler); s.listen(0, "127.0.0.1", () => r(s)); });

test("forwards the exact data string with a signature that passes the documented verification", async () => {
	const data = JSON.stringify(body);
	const api = await listen((req, res) => {
		res.writeHead(200, { "content-type": "text/event-stream" });
		res.write(`retry: 3000\n: connected\n\nid: 1\nevent: goal.met\ndata: ${data}\n\n`);
	});
	const got = [];
	const local = await listen(async (req, res) => {
		let raw = "";
		for await (const c of req) raw += c;
		got.push({ raw, sig: req.headers["percia-signature"] });
		res.writeHead(204).end();
	});
	const ctl = new AbortController();
	const client = createClient({ apiKey: "pk_live_test", baseUrl: `http://127.0.0.1:${api.address().port}` });
	const done = forwardStream({ client, target: `http://127.0.0.1:${local.address().port}/hook`, secret: SECRET, signal: ctl.signal });
	for (let i = 0; i < 200 && got.length < 1; i++) await new Promise((r) => setTimeout(r, 10));
	ctl.abort();
	assert.equal(await done, 1);
	api.closeAllConnections(); api.close(); local.close();

	assert.equal(got[0].raw, data);
	// The verification from docs/integrators/webhooks.md, written out here independently of the SDK.
	const parts = Object.fromEntries(got[0].sig.split(",").map((p) => p.split("=", 2)));
	assert.ok(Math.abs(Date.now() / 1000 - Number(parts.t)) < 300);
	assert.equal(parts.v1, createHmac("sha256", SECRET).update(`${parts.t}.${got[0].raw}`).digest("hex"));
});
