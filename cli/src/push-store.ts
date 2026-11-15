// Where `percia cameras push` keeps publish tokens: <config dir>/push-cameras.json, mode 0600 (directory 0700), written atomically.
// Tokens are bearer secrets for publishing to one camera; they are shown once by the API, so this file is the only copy.
import { chmod, mkdir, readFile, rename, writeFile } from "node:fs/promises";
import { dirname, join } from "node:path";
import { configDir } from "./config.js";
import type { Context } from "./context.js";

export type SavedPushCamera = { cameraId: string; name: string; externalId: string; whipUrl: string; token: string; savedAt: string };
type Store = { version: 1; cameras: Record<string, SavedPushCamera> };

export const pushStorePath = (ctx: Pick<Context, "env" | "platform" | "homedir">) => join(configDir(ctx), "push-cameras.json");
/** One entry per host and external id: the same id on staging and production are different cameras. */
export const storeKey = (baseUrl: string, externalId: string) => `${baseUrl.replace(/\/+$/, "")}|${externalId}`;

async function load(ctx: Context): Promise<Store> {
	try {
		const raw = JSON.parse(await readFile(pushStorePath(ctx), "utf8")) as Store;
		return raw && typeof raw === "object" && raw.cameras ? raw : { version: 1, cameras: {} };
	} catch (e) {
		if ((e as NodeJS.ErrnoException).code === "ENOENT") return { version: 1, cameras: {} };
		throw new Error(`Cannot read ${pushStorePath(ctx)}: ${(e as Error).message}`);
	}
}

async function save(ctx: Context, store: Store): Promise<void> {
	const file = pushStorePath(ctx);
	await mkdir(dirname(file), { recursive: true, mode: 0o700 });
	await chmod(dirname(file), 0o700).catch(() => {});
	const tmp = `${file}.${process.pid}.tmp`;
	await writeFile(tmp, JSON.stringify(store, null, 2) + "\n", { mode: 0o600 });
	await chmod(tmp, 0o600).catch(() => {});
	await rename(tmp, file);
}

export async function getSaved(ctx: Context, baseUrl: string, externalId: string): Promise<SavedPushCamera | undefined> {
	return (await load(ctx)).cameras[storeKey(baseUrl, externalId)];
}
export async function putSaved(ctx: Context, baseUrl: string, entry: SavedPushCamera): Promise<void> {
	const store = await load(ctx);
	store.cameras[storeKey(baseUrl, entry.externalId)] = entry;
	await save(ctx, store);
}
/** Forget the token(s) saved for a camera id (after revoke or remove). Returns how many entries went. */
export async function dropSavedByCameraId(ctx: Context, baseUrl: string, cameraId: string): Promise<number> {
	const store = await load(ctx);
	const prefix = baseUrl.replace(/\/+$/, "") + "|";
	const keys = Object.keys(store.cameras).filter((k) => k.startsWith(prefix) && store.cameras[k]!.cameraId === cameraId);
	for (const k of keys) delete store.cameras[k];
	if (keys.length) await save(ctx, store);
	return keys.length;
}
/** Replace the saved token of a camera id (after rotate). No-op when nothing was saved for it. */
export async function updateSavedToken(ctx: Context, baseUrl: string, cameraId: string, token: string, whipUrl?: string): Promise<boolean> {
	const store = await load(ctx);
	const prefix = baseUrl.replace(/\/+$/, "") + "|";
	let changed = false;
	for (const [k, v] of Object.entries(store.cameras)) {
		if (k.startsWith(prefix) && v.cameraId === cameraId) (store.cameras[k] = { ...v, token, whipUrl: whipUrl ?? v.whipUrl, savedAt: new Date().toISOString() }), (changed = true);
	}
	if (changed) await save(ctx, store);
	return changed;
}
