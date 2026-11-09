import assert from "node:assert/strict";
import { createHmac } from "node:crypto";
import { readFileSync } from "node:fs";
import { test } from "node:test";
import worker, { verifySignature } from "../src/index.js";

const vectors = JSON.parse(readFileSync(new URL("./vectors.json", import.meta.url), "utf8"));

test(`shared vectors (${vectors.cases.length})`, async (t) => {
	for (const c of vectors.cases) {
		await t.test(c.name, async () => {
			const r = await verifySignature(new TextEncoder().encode(c.body), c.header, c.secret, c.now);
			assert.equal(r.ok, c.valid);
			if (!c.valid) assert.equal(r.code, c.code);
		});
	}
});

const SECRET = "whsec_test_worker";
const NOW = 1_793_525_400;
const sign = (body, t) => `t=${t},v1=${createHmac("sha256", SECRET).update(`${t}.${body}`).digest("hex")}`;
const body = JSON.stringify({ id: "dec_9", watchId: "w_1", occurrenceId: "occ_1", type: "goal.met", goal: "A person is at the door", at: "2026-11-01T09:30:00Z" });
const req = (b, sig) => new Request("https://worker.example/", { method: "POST", body: b, headers: sig ? { "percia-signature": sig } : {} });
const ctx = () => { const p = []; return { waitUntil: (x) => p.push(x), p }; };
const fakeKv = () => { const m = new Map(); return { get: async (k) => m.get(k) ?? null, put: async (k, v) => void m.set(k, v) }; };

test("valid delivery is acknowledged and the work is deferred with waitUntil", async () => {
	const c = ctx();
	const res = await worker.fetch(req(body, sign(body, NOW)), { PERCIA_WEBHOOK_SECRET: SECRET }, c, NOW);
	assert.equal(res.status, 200);
	assert.equal(c.p.length, 1);
});

test("bad signature, missing header, stale, tampered: 401", async () => {
	const env = { PERCIA_WEBHOOK_SECRET: SECRET };
	for (const r of [req(body, `t=${NOW},v1=${"a".repeat(64)}`), req(body), req(body, sign(body, NOW - 400)), req(body + " ", sign(body, NOW))]) {
		assert.equal((await worker.fetch(r, env, ctx(), NOW)).status, 401);
	}
});

test("duplicate id with a KV binding answers 2xx and skips the work", async () => {
	const env = { PERCIA_WEBHOOK_SECRET: SECRET, SEEN: fakeKv() };
	const first = ctx();
	await worker.fetch(req(body, sign(body, NOW)), env, first, NOW);
	const second = ctx();
	const res = await worker.fetch(req(body, sign(body, NOW)), env, second, NOW);
	assert.equal(res.status, 200);
	assert.equal((await res.json()).duplicate, true);
	assert.equal(first.p.length, 1);
	assert.equal(second.p.length, 0);
});

test("non-POST is 405 and a missing secret binding is 500", async () => {
	assert.equal((await worker.fetch(new Request("https://w/"), { PERCIA_WEBHOOK_SECRET: SECRET }, ctx(), NOW)).status, 405);
	assert.equal((await worker.fetch(req(body, sign(body, NOW)), {}, ctx(), NOW)).status, 500);
});
