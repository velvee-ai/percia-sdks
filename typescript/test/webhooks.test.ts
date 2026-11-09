import { readFileSync } from "node:fs";
import { describe, expect, it } from "vitest";
import { WebhookSignatureError, assertWebhookSignature, constructWebhookEvent, signWebhook, verifyWebhookSignature } from "../src/index.js";

const vectors = JSON.parse(readFileSync(new URL("../../spec/webhook-vectors.json", import.meta.url), "utf8")) as { tolerance_seconds: number; cases: { name: string; secret: string; body: string; now: number; header: string; valid: boolean; code: string | null }[] };

describe("shared webhook vectors (spec/webhook-vectors.json)", () => {
	for (const c of vectors.cases) {
		it(c.name, async () => {
			expect(await verifyWebhookSignature(c.body, c.header, c.secret, vectors.tolerance_seconds, c.now)).toBe(c.valid);
			if (c.valid) await expect(assertWebhookSignature(c.body, c.header, c.secret, { now: c.now })).resolves.toBeUndefined();
			else await expect(assertWebhookSignature(c.body, c.header, c.secret, { now: c.now })).rejects.toMatchObject({ code: c.code });
		});
	}
});

describe("verifyWebhookSignature", () => {
	const secret = "whsec_unit";
	const body = '{"id":"dec_1","type":"goal.met"}';
	it("round trips with signWebhook", async () => {
		const header = await signWebhook(body, secret, 1_000_000);
		expect(await verifyWebhookSignature(body, header, secret, 300, 1_000_000)).toBe(true);
	});
	it("accepts Uint8Array bodies, Headers, plain objects with any header case, and the bare header value", async () => {
		const header = await signWebhook(body, secret, 1_000_000);
		const bytes = new TextEncoder().encode(body);
		expect(await verifyWebhookSignature(bytes, header, secret, 300, 1_000_000)).toBe(true);
		expect(await verifyWebhookSignature(body, new Headers({ "Percia-Signature": header }), secret, 300, 1_000_000)).toBe(true);
		expect(await verifyWebhookSignature(body, { "PERCIA-SIGNATURE": header }, secret, 300, 1_000_000)).toBe(true);
		expect(await verifyWebhookSignature(body, { "percia-signature": [header] }, secret, 300, 1_000_000)).toBe(true);
	});
	it("rejects a body changed by one byte (re-serialised JSON)", async () => {
		const header = await signWebhook(body, secret, 1_000_000);
		expect(await verifyWebhookSignature(JSON.stringify(JSON.parse(body), null, 1), header, secret, 300, 1_000_000)).toBe(false);
	});
	it("enforces the replay window in both directions and honors a custom tolerance", async () => {
		const header = await signWebhook(body, secret, 1_000_000);
		expect(await verifyWebhookSignature(body, header, secret, 300, 1_000_300)).toBe(true);
		expect(await verifyWebhookSignature(body, header, secret, 300, 1_000_301)).toBe(false);
		expect(await verifyWebhookSignature(body, header, secret, 300, 999_699)).toBe(false);
		expect(await verifyWebhookSignature(body, header, secret, 10, 1_000_011)).toBe(false);
	});
	it("treats missing or malformed headers as malformed, not as a crash", async () => {
		for (const h of [undefined, "", "garbage", "t=abc,v1=00", "t=1", "v1=00", "t=-5,v1=00"]) {
			await expect(assertWebhookSignature(body, h === undefined ? {} : { "percia-signature": h }, secret, { now: 1 })).rejects.toMatchObject({ code: "malformed" });
		}
	});
	it("requires exact lowercase hex, rejects the wrong secret / truncated digest, accepts a repeated v1", async () => {
		const header = await signWebhook(body, secret, 1_000_000);
		expect(await verifyWebhookSignature(body, header.replace(/v1=.*/, (m) => m.toUpperCase().replace("V1=", "v1=")), secret, 300, 1_000_000)).toBe(false);
		expect(await verifyWebhookSignature(body, `${header},v1=${"0".repeat(64)}`, secret, 300, 1_000_000)).toBe(true);
		expect(await verifyWebhookSignature(body, header, "whsec_other", 300, 1_000_000)).toBe(false);
		expect(await verifyWebhookSignature(body, header.slice(0, -2), secret, 300, 1_000_000)).toBe(false);
	});
	it("constructWebhookEvent parses only after verifying", async () => {
		const header = await signWebhook(body, secret);
		expect((await constructWebhookEvent(body, header, secret)).id).toBe("dec_1");
		await expect(constructWebhookEvent("not json", await signWebhook("other", secret), secret)).rejects.toBeInstanceOf(WebhookSignatureError);
	});
});
