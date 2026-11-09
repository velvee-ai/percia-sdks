import { createClient } from "@percia/sdk";
import { DEFAULT_BASE_URL, loadConfig, saveConfig, type Config, type OAuthCredentials } from "./config.js";
import type { Context, GlobalOptions, Session } from "./context.js";
import { CliError, EXIT } from "./errors.js";
import { refresh } from "./oauth.js";

export function resolveBaseUrl(ctx: Context, opts: GlobalOptions, cfg: Config): string {
	return (opts.baseUrl ?? ctx.env.PERCIA_BASE_URL ?? cfg.baseUrl ?? DEFAULT_BASE_URL).replace(/\/+$/, "");
}

/** Build an authenticated SDK client from PERCIA_API_KEY or the stored credentials (refreshing an expiring OAuth token and saving the new one). */
export async function openSession(ctx: Context, opts: GlobalOptions): Promise<Session> {
	const cfg = await loadConfig(ctx);
	const baseUrl = resolveBaseUrl(ctx, opts, cfg);
	const common = { baseUrl, fetch: ctx.fetch, appInfo: "percia-cli", sleep: (ms: number) => ctx.sleep(ms, ctx.signal) };

	if (ctx.env.PERCIA_API_KEY) return { client: createClient({ ...common, apiKey: ctx.env.PERCIA_API_KEY }), baseUrl, auth: "api_key", source: "env" };

	const cred = cfg.credentials;
	if (!cred) throw new CliError("Not logged in.", EXIT.AUTH, "Run `percia login`, or set PERCIA_API_KEY.");
	if (cred.type === "api_key") return { client: createClient({ ...common, apiKey: cred.apiKey }), baseUrl, auth: "api_key", source: "config" };

	let current: OAuthCredentials = cred;
	const token = async () => {
		if (current.expiresAt && current.expiresAt - ctx.now() < 60_000) {
			current = await refresh(ctx, current);
			await saveConfig(ctx, { ...(await loadConfig(ctx)), credentials: current });
		}
		return current.accessToken;
	};
	return { client: createClient({ ...common, oauthToken: token }), baseUrl, auth: "oauth", source: "config" };
}
