// OAuth 2.1 authorization code + PKCE (S256) with dynamic client registration against Percia's issuer.
// Percia advertises no device-authorization grant, so login is the browser flow with a loopback redirect (RFC 8252).
import { createHash, randomBytes } from "node:crypto";
import { createServer, type Server } from "node:http";
import type { AddressInfo } from "node:net";
import type { OAuthCredentials } from "./config.js";
import type { Context } from "./context.js";
import { CliError, EXIT } from "./errors.js";

export const DEFAULT_SCOPES = ["watches:read", "watches:write", "watches:delete", "events:read", "cameras:read", "cameras:write", "integrations:read", "integrations:write", "hooks:write", "offline_access"];
export const READONLY_SCOPES = ["watches:read", "events:read", "cameras:read", "integrations:read", "offline_access"];

export type ServerMetadata = { issuer?: string; authorization_endpoint: string; token_endpoint: string; registration_endpoint: string; revocation_endpoint?: string; scopes_supported?: string[] };

const b64url = (buf: Buffer) => buf.toString("base64url");
export const pkcePair = () => {
	const verifier = b64url(randomBytes(32));
	return { verifier, challenge: b64url(createHash("sha256").update(verifier).digest()) };
};

async function getJson(ctx: Context, url: string): Promise<any | undefined> {
	try {
		const res = await ctx.fetch(url, { headers: { accept: "application/json" } });
		return res.ok ? await res.json() : undefined;
	} catch {
		return undefined;
	}
}

/** Protected-resource metadata -> issuer -> authorization-server metadata. Falls back to `<base>/api/auth` (the documented issuer). */
export async function discover(ctx: Context, baseUrl: string): Promise<ServerMetadata> {
	const origin = new URL(baseUrl).origin;
	const resource = await getJson(ctx, `${origin}/.well-known/oauth-protected-resource`);
	const issuer: string = resource?.authorization_servers?.[0] ?? `${origin}/api/auth`;
	const u = new URL(issuer);
	const candidates = [`${u.origin}/.well-known/oauth-authorization-server${u.pathname === "/" ? "" : u.pathname}`, `${issuer.replace(/\/$/, "")}/.well-known/oauth-authorization-server`, `${u.origin}/.well-known/oauth-authorization-server`, `${issuer.replace(/\/$/, "")}/.well-known/openid-configuration`];
	for (const url of candidates) {
		const meta = await getJson(ctx, url);
		if (meta?.authorization_endpoint && meta?.token_endpoint) {
			if (!meta.registration_endpoint) throw new CliError("The authorization server does not offer dynamic client registration.", EXIT.FAILURE, "Use an API key: percia login --with-key");
			return meta as ServerMetadata;
		}
	}
	throw new CliError(`Could not find OAuth metadata for ${origin}.`, EXIT.NETWORK, "Check the base URL (`percia doctor`), or use an API key: percia login --with-key");
}

async function postForm(ctx: Context, url: string, form: Record<string, string>) {
	const res = await ctx.fetch(url, { method: "POST", headers: { "content-type": "application/x-www-form-urlencoded", accept: "application/json" }, body: new URLSearchParams(form).toString() });
	const body: any = await res.json().catch(() => ({}));
	return { ok: res.ok, status: res.status, body };
}

export async function registerClient(ctx: Context, meta: ServerMetadata, redirectUri: string, scope: string): Promise<string> {
	const res = await ctx.fetch(meta.registration_endpoint, {
		method: "POST",
		headers: { "content-type": "application/json", accept: "application/json" },
		body: JSON.stringify({ client_name: "Percia CLI", redirect_uris: [redirectUri], grant_types: ["authorization_code", "refresh_token"], response_types: ["code"], token_endpoint_auth_method: "none", scope }),
	});
	const body: any = await res.json().catch(() => ({}));
	if (!res.ok || !body.client_id) throw new CliError(`Client registration failed (${res.status}${body.error ? ` ${body.error}` : ""}).`, EXIT.AUTH, "Use an API key: percia login --with-key");
	return body.client_id as string;
}

export type LoginOptions = { baseUrl: string; scopes: string[]; openBrowser: boolean; timeoutMs?: number };

/** Run the browser flow. Returns credentials to store. */
export async function browserLogin(ctx: Context, opts: LoginOptions): Promise<OAuthCredentials> {
	const meta = await discover(ctx, opts.baseUrl);
	const { verifier, challenge } = pkcePair();
	const state = b64url(randomBytes(16));
	const scope = opts.scopes.join(" ");

	let server!: Server;
	const codePromise = new Promise<string>((resolve, reject) => {
		server = createServer((req, res) => {
			const url = new URL(req.url ?? "/", "http://127.0.0.1");
			if (url.pathname !== "/callback") return void res.writeHead(404).end();
			const page = (title: string, text: string) => res.writeHead(200, { "content-type": "text/html; charset=utf-8", "cache-control": "no-store" }).end(`<!doctype html><meta charset="utf-8"><title>${title}</title><body style="font:16px system-ui;margin:3rem"><h1>${title}</h1><p>${text}</p>`);
			if (url.searchParams.get("state") !== state) {
				page("Percia CLI", "State mismatch. Start `percia login` again.");
				return reject(new CliError("Login failed: the redirect carried the wrong state.", EXIT.AUTH));
			}
			const err = url.searchParams.get("error");
			if (err) {
				page("Percia CLI", "Login was not approved. You can close this tab.");
				return reject(new CliError(`Login was not approved (${err.replace(/[^\w .-]/g, "")}).`, EXIT.AUTH));
			}
			const code = url.searchParams.get("code");
			if (!code) return void page("Percia CLI", "No code in the redirect.");
			page("Percia CLI is signed in", "You can close this tab and return to the terminal.");
			resolve(code);
		});
		server.on("error", reject);
	});
	codePromise.catch(() => {}); // the browser may call back before we start waiting; the race below still sees the rejection
	await new Promise<void>((r) => server.listen(0, "127.0.0.1", r));
	const redirectUri = `http://127.0.0.1:${(server.address() as AddressInfo).port}/callback`;
	try {
		const clientId = await registerClient(ctx, meta, redirectUri, scope);
		const authUrl = new URL(meta.authorization_endpoint);
		for (const [k, v] of Object.entries({ response_type: "code", client_id: clientId, redirect_uri: redirectUri, scope, state, code_challenge: challenge, code_challenge_method: "S256" })) authUrl.searchParams.set(k, v);

		const opened = opts.openBrowser ? await ctx.openUrl(authUrl.toString()) : false;
		ctx.stderr(opened ? "Opened your browser to sign in to Percia. If it did not open, use this link:\n" : "Open this link in a browser to sign in to Percia:\n");
		ctx.stderr(`${authUrl.toString()}\n`);
		ctx.stderr(`Waiting for approval on ${redirectUri} (Ctrl-C to cancel)...\n`);

		const timeout = new Promise<never>((_, rej) => {
			const t = setTimeout(() => rej(new CliError("Timed out waiting for the browser sign-in.", EXIT.AUTH)), opts.timeoutMs ?? 5 * 60_000);
			ctx.signal.addEventListener("abort", () => (clearTimeout(t), rej(new CliError("Cancelled.", EXIT.FAILURE))), { once: true });
			codePromise.then(() => clearTimeout(t), () => clearTimeout(t));
		});
		const code = await Promise.race([codePromise, timeout]);
		const tok = await postForm(ctx, meta.token_endpoint, { grant_type: "authorization_code", code, redirect_uri: redirectUri, client_id: clientId, code_verifier: verifier });
		if (!tok.ok || !tok.body.access_token) throw new CliError(`Token exchange failed (${tok.status}${tok.body.error ? ` ${String(tok.body.error).replace(/[^\w .-]/g, "")}` : ""}).`, EXIT.AUTH);
		return {
			type: "oauth",
			clientId,
			accessToken: tok.body.access_token,
			refreshToken: tok.body.refresh_token,
			expiresAt: typeof tok.body.expires_in === "number" ? ctx.now() + tok.body.expires_in * 1000 : undefined,
			scope: tok.body.scope ?? scope,
			tokenEndpoint: meta.token_endpoint,
		};
	} finally {
		server.close();
		server.closeAllConnections?.();
	}
}

/** Refresh an access token. Throws CliError(AUTH) when the refresh token is rejected (the user must log in again). */
export async function refresh(ctx: Context, cred: OAuthCredentials): Promise<OAuthCredentials> {
	if (!cred.refreshToken) throw new CliError("The access token expired and there is no refresh token.", EXIT.AUTH, "Run `percia login`.");
	const tok = await postForm(ctx, cred.tokenEndpoint, { grant_type: "refresh_token", refresh_token: cred.refreshToken, client_id: cred.clientId });
	if (!tok.ok || !tok.body.access_token) throw new CliError("The session could not be refreshed.", EXIT.AUTH, "Run `percia login`.");
	return { ...cred, accessToken: tok.body.access_token, refreshToken: tok.body.refresh_token ?? cred.refreshToken, expiresAt: typeof tok.body.expires_in === "number" ? ctx.now() + tok.body.expires_in * 1000 : undefined, scope: tok.body.scope ?? cred.scope };
}

/** Best-effort revocation (RFC 7009). */
export async function revoke(ctx: Context, baseUrl: string, cred: OAuthCredentials): Promise<boolean> {
	try {
		const meta = await discover(ctx, baseUrl);
		if (!meta.revocation_endpoint) return false;
		const token = cred.refreshToken ?? cred.accessToken;
		const r = await postForm(ctx, meta.revocation_endpoint, { token, client_id: cred.clientId });
		return r.ok;
	} catch {
		return false;
	}
}
