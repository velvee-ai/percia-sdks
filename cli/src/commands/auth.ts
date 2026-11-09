import { Command } from "commander";
import { createClient, PerciaApiError } from "@percia/sdk";
import { clearCredentials, configPath, loadConfig, mask, saveConfig } from "../config.js";
import type { Context, GlobalOptions } from "../context.js";
import { CliError, EXIT } from "../errors.js";
import { browserLogin, DEFAULT_SCOPES, READONLY_SCOPES, revoke } from "../oauth.js";
import { json, table } from "../output.js";
import { openSession, resolveBaseUrl } from "../session.js";

type Deps = { ctx: Context; globals: () => GlobalOptions };

/** Probe the account with read-only calls to learn which scope groups a credential has. Never writes. */
export async function probeScopes(client: ReturnType<typeof createClient>) {
	const probes: [string, () => Promise<unknown>][] = [
		["watches:read", () => client.watches.list()],
		["events:read", () => client.events.list({ limit: 1 })],
		["cameras:read", () => client.cameras.list()],
		["integrations:read", () => client.integrations.list()],
		["hooks:write", () => client.hooks.list()],
	];
	const out: { scope: string; granted: boolean | null; status?: number }[] = [];
	for (const [scope, run] of probes) {
		try {
			await run();
			out.push({ scope, granted: true });
		} catch (e) {
			if (e instanceof PerciaApiError && e.status === 403) out.push({ scope, granted: false, status: 403 });
			else if (e instanceof PerciaApiError && e.status === 404) out.push({ scope, granted: null, status: 404 }); // feature switched off on this host
			else if (e instanceof PerciaApiError && e.status === 401) throw e;
			else out.push({ scope, granted: null });
		}
	}
	return out;
}

export function registerAuth(program: Command, { ctx, globals }: Deps) {
	program
		.command("login")
		.description("Sign in with your browser (OAuth 2.1 + PKCE), or store an API key. PERCIA_API_KEY overrides stored credentials.")
		.option("--with-key", "read an API key from stdin (or a hidden prompt) instead of using the browser")
		.option("--no-browser", "print the sign-in link instead of opening it")
		.option("--scopes <list>", "comma-separated scopes to request (default: everything the CLI uses)")
		.option("--read-only", "request read scopes only")
		.option("--timeout <seconds>", "how long to wait for the browser", (v) => Number(v), 300)
		.action(async (o: { withKey?: boolean; browser: boolean; scopes?: string; readOnly?: boolean; timeout: number }) => {
			const g = globals();
			const cfg = await loadConfig(ctx);
			const baseUrl = resolveBaseUrl(ctx, g, cfg);
			if (o.withKey) {
				const key = (await ctx.readSecret("Paste your API key (input hidden): ")).trim();
				if (!/^pk_[a-z]+_/.test(key)) throw new CliError("That does not look like a Percia API key (expected pk_live_...).", EXIT.USAGE);
				const client = createClient({ baseUrl, apiKey: key, fetch: ctx.fetch, maxRetries: 1 });
				let note: string | undefined;
				try {
					await client.watches.list();
				} catch (e) {
					if (e instanceof PerciaApiError && e.status === 401) throw new CliError("The server rejected that API key.", EXIT.AUTH);
					if (e instanceof PerciaApiError && e.status === 403) note = "Key accepted, but it cannot read watches (missing watches:read).";
					else throw e;
				}
				await saveConfig(ctx, { ...cfg, version: 1, baseUrl: g.baseUrl ?? cfg.baseUrl, credentials: { type: "api_key", apiKey: key } });
				if (g.json) return json(ctx, { ok: true, auth: "api_key", baseUrl, key: mask(key), note });
				ctx.stdout(`Stored API key ${mask(key)} for ${baseUrl} (${configPath(ctx)}, owner-only).\n${note ? note + "\n" : ""}`);
				return;
			}
			const scopes = o.scopes ? o.scopes.split(/[,\s]+/).filter(Boolean) : o.readOnly ? READONLY_SCOPES : DEFAULT_SCOPES;
			const cred = await browserLogin(ctx, { baseUrl, scopes, openBrowser: o.browser, timeoutMs: o.timeout * 1000 });
			await saveConfig(ctx, { ...cfg, version: 1, baseUrl: g.baseUrl ?? cfg.baseUrl, credentials: cred });
			if (g.json) return json(ctx, { ok: true, auth: "oauth", baseUrl, scope: cred.scope, expiresAt: cred.expiresAt ? new Date(cred.expiresAt).toISOString() : null });
			ctx.stdout(`Signed in to ${baseUrl}. Scopes: ${cred.scope}\n`);
		});

	program
		.command("logout")
		.description("Forget the stored credentials (and revoke the OAuth token when possible).")
		.option("--no-revoke", "do not call the revocation endpoint")
		.action(async (o: { revoke: boolean }) => {
			const g = globals();
			const cfg = await loadConfig(ctx);
			let revoked = false;
			if (o.revoke && cfg.credentials?.type === "oauth") revoked = await revoke(ctx, resolveBaseUrl(ctx, g, cfg), cfg.credentials);
			const had = await clearCredentials(ctx);
			if (g.json) return json(ctx, { ok: true, hadCredentials: had, revoked });
			ctx.stdout(had ? `Logged out${revoked ? " and revoked the token" : ""}.\n` : "Nothing to forget.\n");
			if (ctx.env.PERCIA_API_KEY) ctx.stdout("PERCIA_API_KEY is still set in your environment.\n");
		});

	program
		.command("whoami")
		.description("Show which account and permissions the CLI is using.")
		.action(async () => {
			const g = globals();
			const s = await openSession(ctx, g);
			const cfg = await loadConfig(ctx);
			const stored = cfg.credentials?.type === "oauth" && s.source === "config" ? cfg.credentials : undefined;
			let account: { email?: string; name?: string; id?: string } | undefined;
			try {
				const me = (await s.client.account.me()) as { user?: { email?: string; name?: string; id?: string } } | null;
				account = me?.user ?? undefined;
			} catch (e) {
				// /me is a session route: an API key is refused, which is expected.
				if (!(e instanceof PerciaApiError) || e.status === 401 && s.auth === "oauth") throw e;
			}
			const probes = await probeScopes(s.client);
			const granted = probes.filter((p) => p.granted).map((p) => p.scope);
			const result = {
				baseUrl: s.baseUrl,
				auth: s.auth,
				credentialSource: s.source === "env" ? "PERCIA_API_KEY" : "config file",
				account: account ?? null,
				grantedScope: stored?.scope ?? null,
				reachable: probes.map((p) => ({ scope: p.scope, granted: p.granted })),
				expiresAt: stored?.expiresAt ? new Date(stored.expiresAt).toISOString() : null,
			};
			if (g.json) return json(ctx, result);
			ctx.stdout(`Host:        ${s.baseUrl}\nAuth:        ${s.auth === "api_key" ? "API key" : "OAuth token"} (${result.credentialSource})\n`);
			if (account) ctx.stdout(`Account:     ${account.email ?? account.name ?? account.id}\n`);
			if (stored?.scope) ctx.stdout(`Granted:     ${stored.scope}\n`);
			ctx.stdout(`Verified by calling the API (read-only):\n` + table(probes.map((p) => ({ check: p.scope, result: p.granted === true ? "ok" : p.granted === false ? "no access" : "unavailable" })), [{ key: "check" }, { key: "result" }]));
			if (granted.length === 0) throw new CliError("This credential can reach none of the read endpoints.", EXIT.AUTH, "Create a key with the scopes you need, or run `percia login`.");
		});

	const cfgCmd = program.command("config").description("Show where the CLI keeps its settings.");
	cfgCmd.action(async () => {
		const g = globals();
		const cfg = await loadConfig(ctx);
		const view = { path: configPath(ctx), baseUrl: resolveBaseUrl(ctx, g, cfg), credentials: cfg.credentials ? (cfg.credentials.type === "api_key" ? { type: "api_key", key: mask(cfg.credentials.apiKey) } : { type: "oauth", scope: cfg.credentials.scope, expiresAt: cfg.credentials.expiresAt ? new Date(cfg.credentials.expiresAt).toISOString() : null }) : null, env: { PERCIA_API_KEY: ctx.env.PERCIA_API_KEY ? "set" : "unset", PERCIA_BASE_URL: ctx.env.PERCIA_BASE_URL ?? "unset" } };
		if (g.json) return json(ctx, view);
		ctx.stdout(`File:        ${view.path}\nBase URL:    ${view.baseUrl}\nCredentials: ${view.credentials ? JSON.stringify(view.credentials) : "none"}\nPERCIA_API_KEY: ${view.env.PERCIA_API_KEY}\n`);
	});
	cfgCmd
		.command("set-base-url <url>")
		.description("Save the Percia host to use by default.")
		.action(async (url: string) => {
			if (!/^https?:\/\//.test(url)) throw new CliError("The base URL must start with https:// (or http:// for a local worker).", EXIT.USAGE);
			const cfg = await loadConfig(ctx);
			await saveConfig(ctx, { ...cfg, version: 1, baseUrl: url.replace(/\/+$/, "") });
			ctx.stdout(`Base URL set to ${url}\n`);
		});
}
