import { createServer } from "node:http";
import { existsSync, mkdirSync, readFileSync, statSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import type { AddressInfo } from "node:net";
import { afterEach, beforeEach, describe, expect, it } from "vitest";
import { verifyWebhookSignature } from "@percia/sdk";
import { Env, oauthServer } from "./harness.js";

let e: Env;
beforeEach(() => {
	e = new Env();
	e.env.PERCIA_API_KEY = "pk_live_test";
});
afterEach(() => e.cleanup());

const cfgFile = () => join(e.env.PERCIA_CONFIG_DIR!, "config.json");
const mode = (p: string) => statSync(p).mode & 0o777;

describe("login with an API key", () => {
	beforeEach(() => delete e.env.PERCIA_API_KEY);
	it("stores the key owner-only and never prints it", async () => {
		e.secretInput = "pk_live_test\n";
		const r = await e.run("login", "--with-key");
		expect(r.code).toBe(0);
		expect(r.out + r.err).not.toContain("pk_live_test");
		expect(r.out).toContain("pk_live_…test");
		expect(mode(cfgFile())).toBe(0o600);
		expect(mode(dirname(cfgFile()))).toBe(0o700);
		expect((await e.run("watches", "list")).code).toBe(0); // uses the stored key
		expect(e.mock.requests.at(-1)!.headers.get("authorization")).toBe("Bearer pk_live_test");
	});
	it("rejects a key the server refuses (exit 3) and a malformed one (exit 2)", async () => {
		e.secretInput = "pk_live_wrong";
		expect((await e.run("login", "--with-key")).code).toBe(3);
		expect(existsSync(cfgFile())).toBe(false);
		e.secretInput = "hunter2";
		expect((await e.run("login", "--with-key")).code).toBe(2);
	});
	it("logout forgets the key", async () => {
		e.secretInput = "pk_live_test";
		await e.run("login", "--with-key");
		expect((await e.run("logout")).out).toContain("Logged out");
		const r = await e.run("watches", "list");
		expect(r.code).toBe(3);
		expect(r.err).toContain("percia login");
	});
});

describe("login with the browser (OAuth + PKCE)", () => {
	beforeEach(() => delete e.env.PERCIA_API_KEY);
	it("registers a public client, redirects to a loopback port, exchanges the code and stores tokens", async () => {
		const oauth = oauthServer(e);
		const r = await e.run("login", "--scopes", "watches:read,events:read");
		expect(r.err).toContain("Opened your browser");
		expect(r.code, r.err).toBe(0);
		expect(oauth.registrations).toBe(1);
		const au = oauth.lastAuthorize!;
		expect(au.searchParams.get("code_challenge_method")).toBe("S256");
		expect(au.searchParams.get("scope")).toBe("watches:read events:read");
		expect(au.searchParams.get("redirect_uri")).toMatch(/^http:\/\/127\.0\.0\.1:\d+\/callback$/);
		const stored = JSON.parse(readFileSync(cfgFile(), "utf8")).credentials;
		expect(stored.type).toBe("oauth");
		expect(stored.refreshToken).toBe("rt_1");
		expect(mode(cfgFile())).toBe(0o600);
		expect(r.out + r.err).not.toContain(stored.accessToken);
		expect(r.out + r.err).not.toContain("rt_1");
		const l = await e.run("watches", "list");
		expect(l.code, l.err).toBe(0);
		expect(e.mock.requests.at(-1)!.headers.get("authorization")).toBe(`Bearer ${stored.accessToken}`);
	});
	it("--no-browser prints the sign-in link instead of opening a browser", async () => {
		const oauth = oauthServer(e);
		e.onOpen = () => { throw new Error("must not open a browser"); };
		const out: string[] = [];
		const err: string[] = [];
		const { run } = await import("../src/program.js");
		const ctx = e.ctx(out, err);
		const p = run(["--base-url", "https://percia.test", "login", "--no-browser"], ctx);
		// act as the user: wait for the printed link, then visit it
		for (let i = 0; i < 200 && !/https:\/\/percia.test\/api\/auth\/oauth2\/authorize\S+/.test(err.join("")); i++) await new Promise((r) => setTimeout(r, 10));
		const link = /https:\/\/percia.test\/api\/auth\/oauth2\/authorize\S+/.exec(err.join(""))![0];
		expect(e.opened).toEqual([]);
		await e.ctxFetchRaw(link);
		expect(await p).toBe(0);
		expect(err.join("")).toContain("Open this link in a browser");
		expect(oauth.tokens).toHaveLength(1);
	});
	it("a denied approval exits 3 and stores nothing", async () => {
		oauthServer(e, { denies: true });
		const r = await e.run("login");
		expect(r.code).toBe(3);
		expect(r.err).toContain("not approved");
		expect(existsSync(cfgFile())).toBe(false);
	});
	it("a redirect with the wrong state is rejected", async () => {
		oauthServer(e, { wrongState: true });
		const r = await e.run("login");
		expect(r.code).toBe(3);
		expect(r.err).toContain("wrong state");
	});
	it("refreshes an expiring access token, saves the new one, then logout revokes", async () => {
		const oauth = oauthServer(e);
		await e.run("login");
		const cfg = JSON.parse(readFileSync(cfgFile(), "utf8"));
		cfg.credentials.expiresAt = e.now + 10_000; // inside the 60 s refresh margin
		writeFileSync(cfgFile(), JSON.stringify(cfg));
		const r = await e.run("watches", "list");
		expect(r.code, r.err).toBe(0);
		expect(oauth.refreshes).toBe(1);
		expect(e.mock.requests.at(-1)!.headers.get("authorization")).toBe("Bearer at_refreshed_1");
		expect(JSON.parse(readFileSync(cfgFile(), "utf8")).credentials.refreshToken).toBe("rt_2");
		await e.run("logout");
		expect(oauth.revoked).toEqual(["rt_2"]);
	});
	it("a refresh the server rejects asks the user to log in again (exit 3)", async () => {
		oauthServer(e);
		await e.run("login");
		const cfg = JSON.parse(readFileSync(cfgFile(), "utf8"));
		Object.assign(cfg.credentials, { expiresAt: 1, refreshToken: "revoked" });
		writeFileSync(cfgFile(), JSON.stringify(cfg));
		const r = await e.run("watches", "list");
		expect(r.code).toBe(3);
		expect(r.err).toContain("percia login");
	});
});

describe("whoami, doctor, config", () => {
	it("whoami verifies by calling the API and shows no secret", async () => {
		const r = await e.run("whoami", "--json");
		expect(r.code, r.err).toBe(0);
		const j = JSON.parse(r.out);
		expect(j.auth).toBe("api_key");
		expect(j.reachable.find((p: any) => p.scope === "watches:read").granted).toBe(true);
		expect(r.out).not.toContain("pk_live_test");
	});
	it("whoami reports missing scopes", async () => {
		e.env.PERCIA_API_KEY = "pk_ro";
		e.mock.keys.set("pk_ro", ["watches:read"]);
		const j = JSON.parse((await e.run("whoami", "--json")).out);
		expect(j.reachable.find((p: any) => p.scope === "events:read").granted).toBe(false);
	});
	it("doctor passes with a working key and fails without credentials (exit 1)", async () => {
		e.mock.handlers.set("getConfig", () => ({ status: 200, body: { phoneCameraEnabled: true, integrationsEnabled: true } }));
		const ok = await e.run("doctor", "--json");
		expect(ok.code, ok.out).toBe(0);
		expect(JSON.parse(ok.out).checks.some((c: any) => c.name === "sign-in works" && c.status === "ok")).toBe(true);
		delete e.env.PERCIA_API_KEY;
		const bad = await e.run("doctor");
		expect(bad.code).toBe(1);
		expect(bad.out).toContain("FAIL");
	});
	it("doctor warns about a world-readable config file", async () => {
		delete e.env.PERCIA_API_KEY;
		e.secretInput = "pk_live_test";
		await e.run("login", "--with-key");
		(await import("node:fs")).chmodSync(cfgFile(), 0o644);
		const r = await e.run("doctor", "--json");
		expect(JSON.parse(r.out).checks.find((c: any) => c.name === "config file").status).toBe("warn");
	});
	it("config shows a masked key", async () => {
		const r = await e.run("config", "--json");
		expect(JSON.parse(r.out).env.PERCIA_API_KEY).toBe("set");
		expect(r.out).not.toContain("pk_live_test");
	});
});

describe("watches", () => {
	it("create prints the webhook secret once; list/get show none", async () => {
		e.mock.script("createWatch", { status: 201, body: { id: "w_1", displayStatus: "active", webhookSecret: "whsec_abc123", secretHint: "c123" } });
		const r = await e.run("watches", "create", "--source", "rtsp://cam.example.com/s", "--goal", "A person at the door", "--webhook", "https://example.com/hook");
		expect(r.code, r.err).toBe(0);
		expect(r.out).toContain("whsec_abc123");
		expect(e.mock.requests[0].body).toEqual({ sourceUrl: "rtsp://cam.example.com/s", goal: "A person at the door", notify: { type: "webhook", target: "https://example.com/hook" } });
		const list = await e.run("watches", "list");
		expect(list.out).not.toContain("whsec_");
	});
	it("validates usage before calling the API", async () => {
		expect((await e.run("watches", "create", "--source", "rtsp://x")).code).toBe(2);
		expect((await e.run("watches", "create", "--source", "rtsp://x", "--goal", "g", "--agent", "a")).code).toBe(2);
		expect(e.mock.requests).toHaveLength(0);
	});
	it("pause, resume, test, delete (needs --yes without a TTY)", async () => {
		expect((await e.run("watches", "pause", "w_1")).code).toBe(0);
		expect((await e.run("watches", "resume", "w_1")).code).toBe(0);
		expect(e.mock.requests.map((r) => r.body)).toEqual([{ status: "paused" }, { status: "active" }]);
		expect((await e.run("watches", "test", "w_1")).code).toBe(0);
		const refused = await e.run("watches", "delete", "w_1");
		expect(refused.code).toBe(2);
		expect(e.mock.requests.some((r) => r.method === "DELETE")).toBe(false);
		expect((await e.run("watches", "delete", "w_1", "--yes")).code).toBe(0);
		expect(e.mock.requests.at(-1)!.method).toBe("DELETE");
	});
	it("maps API errors to exit codes and prints the request id", async () => {
		e.mock.script("getWatch", { status: 404, body: { error: { code: "not_found", message: "No such watch", request_id: "req_123" }, message: "No such watch" } });
		const nf = await e.run("watches", "get", "nope");
		expect(nf.code).toBe(4);
		expect(nf.err).toContain("req_123");
		e.env.PERCIA_API_KEY = "pk_ro";
		e.mock.keys.set("pk_ro", ["watches:read"]);
		const forbidden = await e.run("watches", "pause", "w_1");
		expect(forbidden.code).toBe(3);
		expect(forbidden.err).toContain("scope");
		const asJson = await e.run("watches", "pause", "w_1", "--json");
		expect(JSON.parse(asJson.err).error.code).toBe("insufficient_scope");
		e.mock.script("listWatches", { status: 429, body: { error: { code: "rate_limited", message: "slow down" }, message: "slow down" }, headers: { "retry-after": "999" } });
		expect((await e.run("watches", "list")).code).toBe(5);
		e.mock.script("listWatches", { status: 500, body: {} }, { status: 500, body: {} }, { status: 500, body: {} });
		expect((await e.run("watches", "list")).code).toBe(7);
	});
	it("network failure exits 6", async () => {
		e.extraFetch = async () => { throw new TypeError("fetch failed"); };
		expect((await e.run("watches", "list")).code).toBe(6);
	});
});

describe("events", () => {
	const ev = (i: number, extra = {}) => ({ id: `evt_${i}`, watchId: "w_1", decisionId: `dec_${i}`, occurrenceId: `occ_${i}`, type: "goal.met", confidence: 0.9, at: "2026-11-01T09:30:00.000Z", deliveryStatus: "delivered", reason: `reason ${i}`, ...extra });
	it("lists, filters and prints no terminal escapes from model text", async () => {
		e.mock.script("listAccountEvents", { status: 200, body: { events: [ev(1, { reason: "\u001b[31mRED\u001b]0;pwn\u0007 text" })], nextCursor: null } });
		const r = await e.run("events", "list", "--watch", "w_1", "--type", "goal.met", "--since", "1793525400", "--limit", "5");
		expect(r.out).not.toContain("\u001b");
		expect(r.out).toContain("RED");
		const q = e.mock.requests[0].url.searchParams;
		expect([q.get("watchId"), q.get("type"), q.get("since"), q.get("limit")]).toEqual(["w_1", "goal.met", "1793525400", "5"]);
	});
	it("--all pages through every event", async () => {
		e.mock.handlers.set("listAccountEvents", (rec) => {
			const c = Number(rec.url.searchParams.get("cursor") ?? 0);
			return { status: 200, body: { events: [ev(c), ev(c + 1)], nextCursor: c < 4 ? String(c + 2) : null } };
		});
		const r = await e.run("events", "list", "--all", "--json");
		expect(JSON.parse(r.out)).toHaveLength(6);
	});
	it("--follow prints the backlog oldest first, then only new events (deduped by id), as NDJSON with --json", async () => {
		const feeds = [
			[ev(2), ev(1)],
			[ev(2), ev(1)],
			[ev(4), ev(3), ev(2), ev(1)],
			[ev(5), ev(4), ev(3), ev(2), ev(1)],
		];
		let i = 0;
		e.mock.handlers.set("listAccountEvents", () => ({ status: 200, body: { events: feeds[Math.min(i++, feeds.length - 1)], nextCursor: null } }));
		e.abortAfterSleeps = 4;
		const r = await e.run("events", "list", "--follow", "--json", "--limit", "2");
		expect(r.code, r.err).toBe(0);
		expect(r.out.trim().split("\n").map((l) => JSON.parse(l).id)).toEqual(["evt_1", "evt_2", "evt_3", "evt_4", "evt_5"]);
	});
	it("rejects a bad --limit", async () => {
		expect((await e.run("events", "list", "--limit", "500")).code).toBe(2);
	});
});

describe("cameras and destinations", () => {
	it("cameras add prints the pairing link and a QR code", async () => {
		e.mock.script("createCamera", { status: 201, body: { camera: { id: "cam_1", name: "Hall" }, pairUrl: "https://percia.test/cam/tok_abc", pairExpiresAt: "2026-11-01T09:40:00.000Z" } });
		const r = await e.run("cameras", "add", "Hall");
		expect(r.out).toContain("https://percia.test/cam/tok_abc");
		expect(r.out).toMatch(/[█▀▄]/);
		expect(r.out).toContain("percia-cam://cam_1");
		const j = JSON.parse((await e.run("cameras", "add", "Hall", "--json")).out);
		expect(j).toBeTruthy();
	});
	it("cameras list and remove", async () => {
		e.mock.script("listCameras", { status: 200, body: [{ id: "cam_1", name: "Hall", status: "online", lastSeenAt: null, watchCount: 1 }] });
		expect((await e.run("cameras", "list")).out).toContain("cam_1");
		e.mock.script("deleteCamera", { status: 409, body: { error: { code: "camera_in_use", message: "in use" }, message: "in use" } });
		expect((await e.run("cameras", "remove", "cam_1")).code).toBe(5);
	});
	it("destinations connect prints the link, validates the service", async () => {
		e.mock.script("listIntegrationServices", { status: 200, body: [{ service: "slack", name: "Slack", available: true, connectKind: "oauth" }, { service: "teams", name: "Teams", available: true, connectKind: "url" }] });
		e.mock.script("createConnectLink", { status: 201, body: { connectUrl: "https://percia.test/connect/abc", expiresAt: "2026-11-01T09:45:00.000Z" } });
		const r = await e.run("destinations", "connect", "slack", "--default");
		expect(r.out).toContain("https://percia.test/connect/abc");
		expect(e.mock.requests.at(-1)!.body).toEqual({ service: "slack", default: true });
		e.mock.script("listIntegrationServices", { status: 200, body: [{ service: "slack", available: true }] });
		const bad = await e.run("destinations", "connect", "myspace");
		expect(bad.code).toBe(2);
		expect(bad.err).toContain("slack");
	});
	it("destinations attach keeps existing rules", async () => {
		e.mock.script("listWatchIntegrations", { status: 200, body: [{ connectionId: "c1", on: "*" }] });
		await e.run("destinations", "attach", "w_1", "c2");
		expect(e.mock.requests.at(-1)!.body).toEqual({ rules: [{ connectionId: "c1", on: "*" }, { connectionId: "c2", on: "*" }] });
	});
});

describe("hooks", () => {
	it("create shows the secret once; refuses non-https", async () => {
		e.mock.script("createHook", { status: 201, body: { id: "hk_1", secret: "whsec_hook" } });
		const r = await e.run("hooks", "create", "https://hooks.zapier.com/x", "--label", "Zap", "--events", "goal.met,*");
		expect(r.out).toContain("whsec_hook");
		expect(e.mock.requests[0].body).toEqual({ url: "https://hooks.zapier.com/x", events: ["goal.met", "*"], label: "Zap" });
		expect((await e.run("hooks", "create", "http://localhost:3000/x")).code).toBe(2);
		e.mock.script("listHooks", { status: 200, body: [{ id: "hk_1", status: "active", events: ["goal.met"] }] });
		expect((await e.run("hooks", "list")).out).not.toContain("whsec_");
		e.mock.script("deleteHook", { status: 200, body: { ok: true, deleted: false } });
		expect((await e.run("hooks", "delete", "hk_1")).out).toContain("already gone");
	});
});

describe("listen", () => {
	async function receiver() {
		const got: { headers: Record<string, any>; body: string }[] = [];
		const server = createServer(async (req, res) => {
			const chunks: Buffer[] = [];
			for await (const c of req) chunks.push(c as Buffer);
			got.push({ headers: req.headers, body: Buffer.concat(chunks).toString("utf8") });
			res.writeHead(204).end();
		});
		await new Promise<void>((r) => server.listen(0, "127.0.0.1", r));
		return { got, url: `http://127.0.0.1:${(server.address() as AddressInfo).port}/hook`, close: () => new Promise<void>((r) => server.close(() => r())) };
	}
	const ev = (i: number) => ({ id: `evt_${i}`, watchId: "w_1", decisionId: `dec_${i}`, occurrenceId: `occ_${i}`, type: "goal.met", confidence: 0.93, at: "2026-11-01T09:30:00.000Z", deliveryStatus: "delivered", reason: "A person in a green jacket." });
	it("forwards new events with the documented body, signed so the SDK verifier accepts it", async () => {
		const rcv = await receiver();
		const feeds = [[ev(1)], [ev(1)], [ev(2), ev(1)]];
		let i = 0;
		e.mock.handlers.set("listAccountEvents", () => ({ status: 200, body: { events: feeds[Math.min(i++, 2)], nextCursor: null } }));
		e.mock.handlers.set("getWatch", () => ({ status: 200, body: { id: "w_1", goal: "A person is standing at the front door" } }));
		e.abortAfterSleeps = 3;
		e.now = 1_793_525_400_000;
		const r = await e.run("listen", "--forward", rcv.url, "--secret", "whsec_mine", "--json");
		await rcv.close();
		expect(r.code, r.err).toBe(0);
		expect(rcv.got).toHaveLength(1); // evt_1 was already there: not forwarded without --replay
		const d = rcv.got[0];
		expect(JSON.parse(d.body)).toEqual({ id: "dec_2", watchId: "w_1", occurrenceId: "occ_2", type: "goal.met", goal: "A person is standing at the front door", reason: "A person in a green jacket.", confidence: 0.93, at: "2026-11-01T09:30:00.000Z" });
		expect(await verifyWebhookSignature(d.body, d.headers, "whsec_mine", 300, 1_793_525_400)).toBe(true);
		expect(await verifyWebhookSignature(d.body, d.headers, "whsec_other", 300, 1_793_525_400)).toBe(false);
		expect(JSON.parse(r.out.trim()).status).toBe(204);
	});
	it("--replay forwards the latest existing events first; a generated secret is printed once", async () => {
		const rcv = await receiver();
		e.mock.handlers.set("listAccountEvents", () => ({ status: 200, body: { events: [ev(2), ev(1)], nextCursor: null } }));
		e.abortAfterSleeps = 1;
		const r = await e.run("listen", "--forward", rcv.url, "--replay", "2");
		await rcv.close();
		expect(rcv.got.map((g) => JSON.parse(g.body).id)).toEqual(["dec_1", "dec_2"]);
		const secret = /whsec_local_[0-9a-f]{32}/.exec(r.err)![0];
		expect(await verifyWebhookSignature(rcv.got[0].body, rcv.got[0].headers, secret)).toBe(true);
		expect(r.err).toContain("not a live relay");
	});
	it("refuses a non-local target unless --allow-remote, and reports a receiver that is down", async () => {
		expect((await e.run("listen", "--forward", "https://example.com/hook")).code).toBe(2);
		expect((await e.run("listen", "--forward", "ftp://localhost/x")).code).toBe(2);
		e.mock.handlers.set("listAccountEvents", () => ({ status: 200, body: { events: [ev(1)], nextCursor: null } }));
		e.abortAfterSleeps = 1;
		const r = await e.run("listen", "--forward", "http://127.0.0.1:1/none", "--replay", "1", "--json");
		expect(JSON.parse(r.out.trim()).status).toBeNull();
	});
});

describe("mcp setup", () => {
	const proj = () => join(e.home, "cwd");
	beforeEach(() => mkdirSync(proj(), { recursive: true }));
	it("claude-code writes ./.mcp.json with no secret by default", async () => {
		const r = await e.run("mcp", "setup", "claude-code");
		expect(r.code, r.err).toBe(0);
		expect(JSON.parse(readFileSync(join(proj(), ".mcp.json"), "utf8"))).toEqual({ mcpServers: { percia: { type: "http", url: "https://percia.test/mcp" } } });
		expect(r.out).toContain("Authenticate");
	});
	it("--with-key references the environment variable, never the key", async () => {
		await e.run("mcp", "setup", "cursor", "--scope", "project", "--with-key");
		const text = readFileSync(join(proj(), ".cursor", "mcp.json"), "utf8");
		expect(text).toContain("${env:PERCIA_API_KEY}");
		expect(text).not.toContain("pk_live_test");
	});
	it("merges without touching other servers, is idempotent, refuses to clobber a different entry", async () => {
		const file = join(proj(), ".mcp.json");
		writeFileSync(file, JSON.stringify({ mcpServers: { other: { command: "x" } }, extra: 1 }));
		await e.run("mcp", "setup", "claude-code");
		const doc = JSON.parse(readFileSync(file, "utf8"));
		expect(doc.mcpServers.other).toEqual({ command: "x" });
		expect(doc.extra).toBe(1);
		expect(existsSync(file + ".percia-bak")).toBe(true);
		expect((await e.run("mcp", "setup", "claude-code")).out).toContain("Already configured");
		const differs = await e.run("mcp", "setup", "claude-code", "--url", "https://other.test/mcp");
		expect(differs.code).toBe(1);
		expect((await e.run("mcp", "setup", "claude-code", "--url", "https://other.test/mcp", "--force")).code).toBe(0);
		expect(JSON.parse(readFileSync(file, "utf8")).mcpServers.percia.url).toBe("https://other.test/mcp");
	});
	it("refuses to overwrite a file that is not valid JSON", async () => {
		writeFileSync(join(proj(), ".mcp.json"), "{ not json");
		expect((await e.run("mcp", "setup", "claude-code")).code).toBe(1);
		expect(readFileSync(join(proj(), ".mcp.json"), "utf8")).toBe("{ not json");
	});
	it("claude-desktop uses mcp-remote; --with-key embeds the key owner-only and --dry-run hides it", async () => {
		const dry = await e.run("mcp", "setup", "claude-desktop", "--with-key", "--dry-run");
		expect(dry.out).not.toContain("pk_live_test");
		expect(dry.out).toContain("<your key>");
		const r = await e.run("mcp", "setup", "claude-desktop", "--with-key");
		expect(r.out).not.toContain("pk_live_test");
		const file = join(e.home, "home", ".config", "Claude", "claude_desktop_config.json");
		const entry = JSON.parse(readFileSync(file, "utf8")).mcpServers.percia;
		expect(entry.command).toBe("npx");
		expect(entry.args).toContain("mcp-remote");
		expect(entry.env.PERCIA_AUTH).toBe("Bearer pk_live_test");
		expect(mode(file)).toBe(0o600);
	});
	it("rejects an unknown target", async () => {
		expect((await e.run("mcp", "setup", "emacs")).code).toBe(2);
	});
});

describe("completion and help", () => {
	it("prints scripts for bash, zsh and fish that list the commands", async () => {
		for (const sh of ["bash", "zsh", "fish"]) {
			const r = await e.run("completion", sh);
			expect(r.code).toBe(0);
			for (const c of ["watches", "events", "listen", "doctor", "mcp"]) expect(r.out).toContain(c);
		}
		expect((await e.run("completion", "powershell")).code).toBe(2);
	});
	it("--help and --version exit 0; an unknown command exits 2", async () => {
		expect((await e.run("--help")).out).toContain("Usage: percia");
		expect((await e.run("--version")).out).toMatch(/\d+\.\d+\.\d+/);
		expect((await e.run("nonsense")).code).toBe(2);
	});
});
