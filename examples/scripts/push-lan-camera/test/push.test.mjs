// Offline end-to-end: a mock Percia API (the recorded contract) + a fake ffmpeg that records its arguments.
// Needs the SDK built once: pnpm --filter @percia/sdk build   (skipped otherwise).
import assert from "node:assert/strict";
import { spawn } from "node:child_process";
import { chmodSync, existsSync, mkdtempSync, readFileSync, statSync, writeFileSync } from "node:fs";
import { createServer } from "node:http";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { test } from "node:test";
import { fileURLToPath } from "node:url";

const here = fileURLToPath(new URL(".", import.meta.url));
const contract = JSON.parse(readFileSync(join(here, "../../../../spec/camera-push-contract.json"), "utf8"));
const built = existsSync(join(here, "../../../../typescript/dist/index.js"));
const TOKEN = contract.register.created.body.token;

async function withMock(handler, fn) {
	const calls = [];
	const server = createServer(async (req, res) => {
		let body = "";
		for await (const c of req) body += c;
		calls.push({ method: req.method, url: req.url, auth: req.headers.authorization, body: body ? JSON.parse(body) : undefined });
		const out = handler(req, calls.at(-1));
		res.writeHead(out.status, { "content-type": "application/json" });
		res.end(out.body === undefined ? "" : JSON.stringify(out.body));
	});
	await new Promise((r) => server.listen(0, "127.0.0.1", r));
	try { return await fn(`http://127.0.0.1:${server.address().port}`, calls); } finally { server.close(); }
}

function run(base, dir, extra = {}) {
	const fake = join(dir, "ffmpeg");
	writeFileSync(fake, `#!/bin/sh\nprintf '%s\\n' "$@" > "${join(dir, "argv.txt")}"\necho "WHIP ok token ${TOKEN}" >&2\n`);
	chmodSync(fake, 0o755);
	const env = { ...process.env, PERCIA_API_KEY: "pk_live_test", PERCIA_BASE_URL: base, RTSP_URL: "rtsp://admin:s3cret@192.168.1.20/s1", FFMPEG: fake, TOKEN_FILE: join(dir, "token"), ONCE: "1", ...extra };
	return new Promise((resolve) => {
		const child = spawn(process.execPath, ["--import", join(here, "resolve-sdk.mjs"), join(here, "../push.mjs")], { env, cwd: dir });
		let err = "";
		child.stderr.on("data", (d) => (err += d));
		child.on("close", (code) => resolve({ code, err }));
	});
}

const mock = (existing) => (req) => {
	if (req.url === "/api/cameras" && req.method === "POST") return existing ? contract.register.existing : contract.register.created;
	if (req.url.endsWith("/token")) return contract.rotate;
	if (req.url === "/api/cam/heartbeat") return { status: 204 };
	return { status: 404, body: { error: { code: "not_found", message: "x" } } };
};

test("registers, saves the token 0600, runs ffmpeg with it, never prints it or the RTSP password", { skip: !built && "build the SDK first" }, async () => {
	const dir = mkdtempSync(join(tmpdir(), "percia-ex-"));
	await withMock(mock(false), async (base, calls) => {
		const r = await run(base, dir);
		assert.equal(r.code, 0, r.err);
		assert.equal(calls[0].body.kind, "push");
		assert.match(calls[0].body.externalId, /^example-192\.168\.1\.20-[0-9a-f]{6}$/);
		assert.equal(readFileSync(join(dir, "token"), "utf8").trim(), TOKEN);
		assert.equal(statSync(join(dir, "token")).mode & 0o777, 0o600);
		const argv = readFileSync(join(dir, "argv.txt"), "utf8").split("\n");
		assert.ok(argv.includes(TOKEN) && argv.includes("whip") && argv.includes(contract.register.created.body.whipUrl));
		assert.ok(!r.err.includes(TOKEN) && !r.err.includes("s3cret"), "token or password leaked: " + r.err);
		assert.ok(r.err.includes("[token]"));
		assert.equal(calls.find((c) => c.url === "/api/cam/heartbeat").auth, `Bearer ${TOKEN}`);
	});
});

test("a rerun uses the saved token; without one it explains and exits 1", { skip: !built && "build the SDK first" }, async () => {
	const dir = mkdtempSync(join(tmpdir(), "percia-ex-"));
	await withMock(mock(true), async (base) => {
		const lost = await run(base, dir);
		assert.equal(lost.code, 1);
		assert.match(lost.err, /ROTATE=1/);
		writeFileSync(join(dir, "token"), TOKEN + "\n", { mode: 0o600 });
		assert.equal((await run(base, dir)).code, 0);
		const rotated = await run(base, mkdtempSync(join(tmpdir(), "percia-ex-")), { ROTATE: "1" });
		assert.equal(rotated.code, 0, rotated.err);
	});
});
