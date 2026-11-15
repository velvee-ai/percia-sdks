import { mkdtempSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { createHash, randomBytes } from "node:crypto";
import { run } from "../src/program.js";
import type { Context } from "../src/context.js";
import { MockPercia } from "../../typescript/test/mock-server.js";

export type Result = { code: number; out: string; err: string };

export class Env {
	mock = new MockPercia();
	home = mkdtempSync(join(tmpdir(), "percia-cli-"));
	env: Record<string, string | undefined> = { PERCIA_CONFIG_DIR: join(this.home, "config") };
	secretInput = "";
	opened: string[] = [];
	/** Called when the CLI "opens the browser". Default: do nothing. */
	onOpen: (url: string) => Promise<void> | void = () => {};
	sleeps = 0;
	/** Abort the run (as Ctrl-C would) after this many sleeps; used to end --follow and listen loops. */
	abortAfterSleeps = Infinity;
	ctl = new AbortController();
	extraFetch?: (req: Request) => Promise<Response | undefined>;
	now = Date.now();
	/** What `ffmpeg -muxers` prints (undefined = not installed). */
	ffmpegMuxers: string | undefined = " E whip            WHIP(WebRTC-HTTP ingestion protocol) muxer\n";
	/** Every foreground program started: command, argv. */
	execs: { cmd: string; args: string[] }[] = [];
	/** Decide how a foreground program ends; default: exit 0. May write to `onStderr`. */
	onExec: (cmd: string, args: string[], onStderr: (c: string) => void) => Promise<{ code: number | null; startError?: string }> = async () => ({ code: 0 });

	ctx(out: string[], err: string[]): Context {
		return {
			argv0: "percia",
			stdout: (t) => void out.push(t),
			stderr: (t) => void err.push(t),
			env: this.env,
			platform: "linux",
			cwd: join(this.home, "cwd"),
			homedir: join(this.home, "home"),
			isTTY: false,
			fetch: (async (input: RequestInfo | URL, init?: RequestInit) => {
				const req = new Request(input as RequestInfo, init);
				if (new URL(req.url).host !== "percia.test") return fetch(req); // a local receiver: real network on loopback
				const extra = await this.extraFetch?.(req.clone());
				return extra ?? this.mock.handle(req);
			}) as typeof fetch,
			now: () => this.now,
			sleep: async () => {
				if (++this.sleeps >= this.abortAfterSleeps) this.ctl.abort();
			},
			openUrl: async (u) => (this.opened.push(u), await this.onOpen(u), true),
			readSecret: async () => this.secretInput,
			capture: async (cmd) => (cmd === "ffmpeg" && this.ffmpegMuxers !== undefined ? { code: 0, stdout: this.ffmpegMuxers, stderr: "" } : undefined),
			exec: async (cmd, args, o) => (this.execs.push({ cmd, args }), this.onExec(cmd, args, (c) => o.onStderr?.(c))),
			signal: this.ctl.signal,
		};
	}

	async run(...argv: string[]): Promise<Result> {
		const out: string[] = [];
		const err: string[] = [];
		const code = await run(["--base-url", "https://percia.test", ...argv], this.ctx(out, err));
		return { code, out: out.join(""), err: err.join("") };
	}
	/** Resolve an authorize URL like a browser: the fake server answers 302 to the loopback redirect, which is then fetched over real HTTP. */
	async ctxFetchRaw(url: string) {
		const r = await this.extraFetch!(new Request(url));
		const loc = r?.headers.get("location");
		return loc ? fetch(loc) : undefined;
	}
	cleanup() { rmSync(this.home, { recursive: true, force: true }); }
}

/** A fake authorization server: discovery, registration, authorize (the "browser" calls the redirect), token, refresh, revoke. */
export function oauthServer(env: Env, opts: { denies?: boolean; wrongState?: boolean } = {}) {
	const state = { clients: new Map<string, { redirect: string }>(), codes: new Map<string, { challenge: string; clientId: string }>(), tokens: [] as string[], refreshes: 0, revoked: [] as string[], registrations: 0, lastAuthorize: undefined as URL | undefined };
	const base = "https://percia.test";
	env.extraFetch = async (req) => {
		const u = new URL(req.url);
		if (u.pathname === "/.well-known/oauth-protected-resource") return Response.json({ resource: `${base}/mcp`, authorization_servers: [`${base}/api/auth`] });
		if (u.pathname.endsWith("/.well-known/oauth-authorization-server") || u.pathname.includes("/.well-known/oauth-authorization-server/"))
			return Response.json({ issuer: `${base}/api/auth`, authorization_endpoint: `${base}/api/auth/oauth2/authorize`, token_endpoint: `${base}/api/auth/oauth2/token`, registration_endpoint: `${base}/api/auth/oauth2/register`, revocation_endpoint: `${base}/api/auth/oauth2/revoke` });
		if (u.pathname === "/api/auth/oauth2/register") {
			const body: any = await req.json();
			state.registrations++;
			if (body.token_endpoint_auth_method !== "none" || !body.redirect_uris?.[0]?.startsWith("http://127.0.0.1:")) return Response.json({ error: "invalid_client_metadata" }, { status: 400 });
			const clientId = "cli_" + randomBytes(4).toString("hex");
			state.clients.set(clientId, { redirect: body.redirect_uris[0] });
			return Response.json({ client_id: clientId }, { status: 201 });
		}
		if (u.pathname === "/api/auth/oauth2/authorize") {
			state.lastAuthorize = u;
			const clientId = u.searchParams.get("client_id")!;
			if (u.searchParams.get("code_challenge_method") !== "S256") return new Response("no pkce", { status: 400 });
			const redirect = new URL(state.clients.get(clientId)!.redirect);
			if (opts.denies) redirect.searchParams.set("error", "access_denied");
			else {
				const code = "code_" + randomBytes(4).toString("hex");
				state.codes.set(code, { challenge: u.searchParams.get("code_challenge")!, clientId });
				redirect.searchParams.set("code", code);
			}
			redirect.searchParams.set("state", opts.wrongState ? "tampered" : u.searchParams.get("state")!);
			return Response.redirect(redirect.toString(), 302);
		}
		if (u.pathname === "/api/auth/oauth2/token") {
			const form = new URLSearchParams(await req.text());
			if (form.get("grant_type") === "refresh_token") {
				state.refreshes++;
				if (form.get("refresh_token") !== "rt_1" && form.get("refresh_token") !== "rt_2") return Response.json({ error: "invalid_grant" }, { status: 400 });
				const access = `at_refreshed_${state.refreshes}`;
				env.mock.keys.set(access, ["watches:read", "events:read", "cameras:read", "integrations:read", "hooks:write", "watches:write"]);
				return Response.json({ access_token: access, refresh_token: "rt_2", expires_in: 3600, scope: "watches:read" });
			}
			const c = state.codes.get(form.get("code") ?? "");
			if (!c || createHash("sha256").update(form.get("code_verifier") ?? "").digest("base64url") !== c.challenge || form.get("client_id") !== c.clientId) return Response.json({ error: "invalid_grant" }, { status: 400 });
			state.codes.delete(form.get("code")!);
			const access = "at_" + randomBytes(4).toString("hex");
			state.tokens.push(access);
			env.mock.keys.set(access, ["watches:read", "events:read", "cameras:read", "integrations:read", "hooks:write", "watches:write", "watches:delete", "cameras:write", "integrations:write"]);
			return Response.json({ access_token: access, refresh_token: "rt_1", expires_in: 3600, scope: (state.lastAuthorize?.searchParams.get("scope") ?? "") });
		}
		if (u.pathname === "/api/auth/oauth2/revoke") {
			state.revoked.push(new URLSearchParams(await req.text()).get("token")!);
			return new Response(null, { status: 200 });
		}
		return undefined;
	};
	// The "browser": follow the authorize URL, which redirects to the CLI's loopback server (real HTTP).
	env.onOpen = async (url) => void (await env.ctxFetchRaw(url));
	return state;
}
