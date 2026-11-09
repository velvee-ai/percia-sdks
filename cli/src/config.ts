import { chmod, mkdir, readFile, rename, rm, writeFile } from "node:fs/promises";
import { dirname, join } from "node:path";
import type { Context } from "./context.js";

export type OAuthCredentials = {
	type: "oauth";
	clientId: string;
	accessToken: string;
	refreshToken?: string;
	/** Unix ms when the access token expires. */
	expiresAt?: number;
	scope?: string;
	tokenEndpoint: string;
};
export type ApiKeyCredentials = { type: "api_key"; apiKey: string };
export type Credentials = OAuthCredentials | ApiKeyCredentials;
export type Config = { version: 1; baseUrl?: string; credentials?: Credentials };

export const DEFAULT_BASE_URL = "https://playground.percia.ai";

/** OS config directory: macOS ~/Library/Application Support/percia, Windows %APPDATA%\percia, else $XDG_CONFIG_HOME or ~/.config/percia. */
export function configDir(ctx: Pick<Context, "env" | "platform" | "homedir">): string {
	if (ctx.env.PERCIA_CONFIG_DIR) return ctx.env.PERCIA_CONFIG_DIR;
	if (ctx.platform === "darwin") return join(ctx.homedir, "Library", "Application Support", "percia");
	if (ctx.platform === "win32") return join(ctx.env.APPDATA ?? join(ctx.homedir, "AppData", "Roaming"), "percia");
	return join(ctx.env.XDG_CONFIG_HOME ?? join(ctx.homedir, ".config"), "percia");
}
export const configPath = (ctx: Pick<Context, "env" | "platform" | "homedir">) => join(configDir(ctx), "config.json");

export async function loadConfig(ctx: Context): Promise<Config> {
	try {
		const raw = JSON.parse(await readFile(configPath(ctx), "utf8")) as Config;
		return raw && typeof raw === "object" ? { ...raw, version: 1 } : { version: 1 };
	} catch (e) {
		if ((e as NodeJS.ErrnoException).code === "ENOENT") return { version: 1 };
		throw new Error(`Cannot read ${configPath(ctx)}: ${(e as Error).message}`);
	}
}

/** Atomic write with owner-only permissions (0600 file, 0700 directory). On Windows the mode bits are advisory; the profile directory is already per-user. */
export async function saveConfig(ctx: Context, config: Config): Promise<void> {
	const file = configPath(ctx);
	await mkdir(dirname(file), { recursive: true, mode: 0o700 });
	await chmod(dirname(file), 0o700).catch(() => {});
	const tmp = `${file}.${process.pid}.tmp`;
	await writeFile(tmp, JSON.stringify(config, null, 2) + "\n", { mode: 0o600 });
	await chmod(tmp, 0o600).catch(() => {});
	await rename(tmp, file);
}

export async function clearCredentials(ctx: Context): Promise<boolean> {
	const cfg = await loadConfig(ctx);
	if (!cfg.credentials) return false;
	delete cfg.credentials;
	if (!cfg.baseUrl) await rm(configPath(ctx), { force: true });
	else await saveConfig(ctx, cfg);
	return true;
}

/** Last four characters only, e.g. `pk_live_…a1b2`. For display; never print more. */
export function mask(secret: string | undefined): string {
	if (!secret) return "";
	return secret.length <= 8 ? "••••" : `${secret.slice(0, secret.startsWith("pk_live_") ? 8 : 0)}…${secret.slice(-4)}`;
}
