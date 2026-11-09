import assert from "node:assert/strict";
import { createHmac } from "node:crypto";
import { test } from "node:test";
import { createReceiver } from "../receiver.mjs";
import { escapeSlack, formatSlackMessage } from "../slack.mjs";

const event = { id: "dec_1", watchId: "w_abc", type: "goal.met", goal: "A package has been left at the front door", reason: "A brown box sits on the mat.", confidence: 0.93, at: "2026-11-01T09:30:00Z" };

test("formats a Block Kit message", () => {
	const m = formatSlackMessage(event);
	assert.equal(m.text, event.goal);
	assert.deepEqual(m.blocks.map((b) => b.type), ["header", "section", "context"]);
	assert.match(m.blocks[1].text.text, /\*A package has been left at the front door\*\n>A brown box sits on the mat\./);
	assert.match(JSON.stringify(m.blocks[2]), /93%/);
	assert.ok(JSON.stringify(m.blocks[2]).includes(`<!date^${Math.floor(Date.parse(event.at) / 1000)}^`));
});

test("escapes Slack control sequences in untrusted reason text", () => {
	const m = formatSlackMessage({ ...event, reason: "<!channel> look <https://evil.example|click> & more" });
	const text = m.blocks[1].text.text;
	assert.ok(!text.includes("<!channel>") && !text.includes("<https://"));
	assert.match(text, /&lt;!channel&gt; look &lt;https:\/\/evil\.example\|click&gt; &amp; more/);
	assert.equal(escapeSlack(null), "");
});

test("clips long reasons and survives missing fields", () => {
	const m = formatSlackMessage({ id: "x", reason: "a".repeat(2000) });
	assert.ok(m.blocks[1].text.text.length < 400);
	assert.equal(m.text, "Goal met");
	assert.ok(m.blocks[2].elements.length >= 1);
});

test("image only when opted in and https", () => {
	const withImage = { ...event, imageUrl: "https://img.example/abc" };
	assert.equal(formatSlackMessage(withImage).blocks.some((b) => b.type === "image"), false);
	assert.equal(formatSlackMessage(withImage, { includeImage: true }).blocks.some((b) => b.type === "image"), true);
	assert.equal(formatSlackMessage({ ...event, imageUrl: "javascript:alert(1)" }, { includeImage: true }).blocks.some((b) => b.type === "image"), false);
});

test("receiver verifies, forwards once, and acknowledges duplicates", async () => {
	const SECRET = "whsec_test_slack";
	const NOW = 1_793_525_400;
	const forwarded = [];
	const server = createReceiver({ secret: SECRET, now: () => NOW, forward: async (m) => void forwarded.push(m) });
	await new Promise((r) => server.listen(0, "127.0.0.1", r));
	const url = `http://127.0.0.1:${server.address().port}/hooks/percia`;
	const body = JSON.stringify(event);
	const sig = `t=${NOW},v1=${createHmac("sha256", SECRET).update(`${NOW}.${body}`).digest("hex")}`;
	try {
		assert.equal((await fetch(url, { method: "POST", body, headers: { "percia-signature": sig } })).status, 200);
		assert.equal((await fetch(url, { method: "POST", body, headers: { "percia-signature": sig } })).status, 200);
		assert.equal((await fetch(url, { method: "POST", body, headers: { "percia-signature": `t=${NOW},v1=${"0".repeat(64)}` } })).status, 401);
		await new Promise((r) => setTimeout(r, 20));
		assert.equal(forwarded.length, 1);
	} finally { await new Promise((r) => server.close(r)); }
});
