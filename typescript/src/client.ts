import { createClient as createGeneratedClient, createConfig } from "./generated/client/index.js";
import type { Client } from "./generated/client/index.js";
import * as sdk from "./generated/sdk.gen.js";
import type { Camera, Event, EventPage, Watch } from "./generated/types.gen.js";
import { NotFoundError, PerciaError, errorFromResponse } from "./errors.js";
import { billingOf, type Billing, type Plan } from "./billing.js";
import type { BulkItem, BulkResult, CameraStatus, PushRegistration } from "./push.js";
import { createRetryingFetch, type RetryOptions } from "./retry.js";
import { paginate } from "./pagination.js";
import { streamEvents, type EventStreamOptions, type StreamDeps } from "./stream.js";

export const DEFAULT_BASE_URL = "https://playground.percia.ai";
export const SDK_VERSION = "0.3.2";

export type TokenSource = string | (() => string | Promise<string>);

export type PerciaClientOptions = RetryOptions & {
	/** API key (`pk_live_...`). Exactly one of `apiKey` and `oauthToken`. Never put a key in browser code. */
	apiKey?: TokenSource;
	/** OAuth 2.1 access token. May be a function, called per request, so you can refresh it. */
	oauthToken?: TokenSource;
	/** Origin of your Percia host, e.g. `https://playground.percia.ai`. `/api` is appended unless present. */
	baseUrl?: string;
	/** Custom fetch (tests, proxies, Workers service bindings). Default: global fetch. */
	fetch?: typeof fetch;
	/** Extra headers on every request. */
	headers?: Record<string, string>;
	/** Appended to the User-Agent-style `x-percia-client` header. */
	appInfo?: string;
};

export function normalizeBaseUrl(baseUrl: string = DEFAULT_BASE_URL): string {
	const trimmed = baseUrl.trim().replace(/\/+$/, "");
	return /\/api$/.test(trimmed) ? trimmed : `${trimmed}/api`;
}

type Unwrapped<T> = T extends { data: infer D } ? Exclude<D, undefined> : never;

/** Turn the generated `{data, error, response}` result into the value or a typed `PerciaApiError`. */
export async function unwrap<R extends { data?: unknown; error?: unknown; response?: Response }>(p: R | Promise<R>): Promise<NonNullable<R["data"]>> {
	const r = await p;
	if (r.error !== undefined || (r.response && !r.response.ok)) {
		if (r.error instanceof Error) throw r.error; // thrown by fetch (connection, timeout, abort): already typed by the retry layer
		throw r.response ? errorFromResponse(r.response, r.error) : new PerciaError(`Request failed: ${String(r.error)}`);
	}
	return r.data as NonNullable<R["data"]>;
}

type Bound<F> = F extends (options: infer O) => infer R ? (options: Omit<NonNullable<O>, "client"> & { client?: Client }) => R : F;
type BoundSdk = { [K in keyof typeof sdk]: (typeof sdk)[K] };

export type ListEventsParams = { watchId?: string; type?: string; since?: string | number | Date; limit?: number; cursor?: string };

export class PerciaClient {
	/** The generated, fully typed client. Use with the generated operation functions via `client.api`. */
	readonly raw: Client;
	/** Every operation, by operationId, with this client pre-bound. They return `{ data, error, response }` and do not throw. */
	readonly api: BoundSdk;
	readonly baseUrl: string;
	/** What `events.stream` needs: the same credentials and headers, but the bare fetch (a stream must not be retried as a request). */
	/** @internal */
	readonly streamDeps: StreamDeps;
	/** @internal */
	readonly streamDefaults: Pick<EventStreamOptions, "sleep" | "random" | "baseDelayMs">;

	readonly watches: Watches;
	readonly events: Events;
	readonly cameras: Cameras;
	readonly integrations: Integrations;
	readonly hooks: Hooks;
	readonly account: Account;

	constructor(options: PerciaClientOptions = {}) {
		if (options.apiKey && options.oauthToken) throw new PerciaError("Pass either apiKey or oauthToken, not both.");
		const token = options.apiKey ?? options.oauthToken;
		this.baseUrl = normalizeBaseUrl(options.baseUrl);
		const baseFetch = options.fetch ?? ((input: RequestInfo | URL, init?: RequestInit) => globalThis.fetch(input, init));
		const extra = options.headers ?? {};
		const fetchWithRetry = createRetryingFetch(baseFetch, {
			...options,
			prepare: async (req) => {
				const value = typeof token === "function" ? await token() : token;
				if (value) req.headers.set("authorization", `Bearer ${value}`);
				req.headers.set("x-percia-client", `percia-sdk-js/${SDK_VERSION}${options.appInfo ? ` ${options.appInfo}` : ""}`);
				for (const [k, v] of Object.entries(extra)) req.headers.set(k, v);
				return req;
			},
		});
		this.streamDefaults = { sleep: options.sleep, random: options.random, baseDelayMs: options.baseDelayMs };
		this.streamDeps = {
			baseUrl: this.baseUrl,
			fetch: baseFetch as typeof fetch,
			headers: async () => {
				const value = typeof token === "function" ? await token() : token;
				return { ...(value ? { authorization: `Bearer ${value}` } : {}), "x-percia-client": `percia-sdk-js/${SDK_VERSION}${options.appInfo ? ` ${options.appInfo}` : ""}`, ...extra };
			},
		};
		this.raw = createGeneratedClient(createConfig({ baseUrl: this.baseUrl, fetch: fetchWithRetry as typeof fetch }));
		const bound: Record<string, unknown> = {};
		for (const [name, fn] of Object.entries(sdk)) {
			if (typeof fn === "function") bound[name] = (opts: Record<string, unknown> = {}) => (fn as (o: unknown) => unknown)({ client: this.raw, ...opts });
		}
		this.api = bound as unknown as BoundSdk;
		this.watches = new Watches(this);
		this.events = new Events(this);
		this.cameras = new Cameras(this);
		this.integrations = new Integrations(this);
		this.hooks = new Hooks(this);
		this.account = new Account(this);
	}
}

export function createClient(options: PerciaClientOptions = {}): PerciaClient {
	return new PerciaClient(options);
}

const toSince = (s: ListEventsParams["since"]) => (s instanceof Date ? s.toISOString() : s === undefined ? undefined : String(s));

type Body<K extends keyof typeof sdk> = (typeof sdk)[K] extends (o: infer O) => unknown ? O extends { body: infer B } ? B : never : never;

class Watches {
	constructor(private c: PerciaClient) {}
	/** Your watches. Not paginated by the API. */
	list() { return unwrap(this.c.api.listWatches({})); }
	/** Async iterator over your watches (one page today; stable if the API adds paging). */
	async *iterate(): AsyncGenerator<Watch, void, void> { for (const w of await this.list()) yield w; }
	get(id: string) { return unwrap(this.c.api.getWatch({ path: { id } })); }
	/**
	 * Create a watch. The response is the only time `webhookSecret` is shown: store it.
	 * A clear goal creates the watch; an unclear one answers 422 `clarification_needed` (see the API docs). Parts that cannot be watched
	 * answer 409 `unsupported_not_acknowledged`: tell the person, then repeat with `acknowledgeUnsupported: true`.
	 */
	create(body: Body<"createWatch">) { return unwrap(this.c.api.createWatch({ body })); }
	update(id: string, body: Body<"updateWatch">) { return unwrap(this.c.api.updateWatch({ path: { id }, body })); }
	pause(id: string) { return this.update(id, { status: "paused" } as Body<"updateWatch">); }
	resume(id: string) { return this.update(id, { status: "active" } as Body<"updateWatch">); }
	delete(id: string) { return unwrap(this.c.api.deleteWatch({ path: { id } })); }
	/** Send a signed test event to the watch's webhook target. */
	testDelivery(id: string) { return unwrap(this.c.api.testWatchDelivery({ path: { id } })); }
	/** Replaces the secret immediately (no overlap). Returns the new `webhookSecret` once. */
	rotateSecret(id: string) { return unwrap(this.c.api.rotateWatchSecret({ path: { id } })); }
	/** One page of this watch's events, newest first. */
	listEvents(id: string, query: { limit?: number; cursor?: string } = {}) { return unwrap(this.c.api.listWatchEvents({ path: { id }, query })); }
	/** Every event of one watch, newest first, following `nextCursor`. */
	iterateEvents(id: string, query: { limit?: number; cursor?: string } = {}) {
		return paginate<Event>((cursor) => this.listEvents(id, { ...query, cursor: cursor ?? query.cursor }));
	}
}

class Events {
	constructor(private c: PerciaClient) {}
	/** One page of the account-wide feed (all watches), newest first. */
	list(params: ListEventsParams = {}): Promise<EventPage> {
		const { since, ...rest } = params;
		return unwrap(this.c.api.listAccountEvents({ query: { ...rest, since: toSince(since) } }));
	}
	/** Every event matching the filters, newest first, following `nextCursor`. Stop with `break`; the loop is lazy. */
	iterate(params: ListEventsParams = {}) {
		return paginate<Event>((cursor) => this.list({ ...params, cursor: cursor ?? params.cursor }));
	}
	/**
	 * Follow the developer event feed (`GET /api/events/stream`, Server-Sent Events) for local development and tests, not as a delivery path.
	 * An async iterator that reconnects with the last cursor, honours `Retry-After`, dedupes on `eventId` and ends when `signal` aborts.
	 * Needs `events:read`. See `EventStreamOptions` and `StreamItem`.
	 */
	stream(options: EventStreamOptions = {}) {
		return streamEvents(this.c.streamDeps, { ...this.c.streamDefaults, ...options });
	}
	/** One example event in the feed's shape (for editors that need sample data). Not a real event. */
	sample() { return unwrap(this.c.api.getSampleEvent({})); }
}

export type RegisterPushOptions = {
	name: string;
	/** Your own stable id for this camera (1-100 chars of `A-Za-z0-9._:-`). Re-registering the same id returns the same camera. */
	externalId: string;
	/**
	 * What to do when the camera already exists (HTTP 200, the server never returns its token again):
	 * `"return"` (default) gives `{ existing: true, token: null }`; `"rotate"` mints a new token (the old one stops working);
	 * `"throw"` raises a `PerciaError` so a script that needs a token cannot continue without one.
	 */
	onExisting?: "return" | "rotate" | "throw";
};

/** The server accepts 1 to 10 cameras per bulk request. */
const BULK_MAX = 10;

type PushResponse = { camera?: Camera; whipUrl?: string; token?: string | null; existing?: boolean; publish?: Record<string, unknown> };

function toRegistration(res: PushResponse): PushRegistration {
	if (!res.camera?.id || !res.whipUrl) throw new PerciaError("Percia did not return a push camera (no id or whipUrl). Is the server new enough for kind: \"push\"?");
	return { camera: res.camera, whipUrl: res.whipUrl, token: res.token ?? null, existing: res.existing === true, rotated: false, publish: res.publish };
}

/** Status of a camera from a `GET /cameras` row, for servers that have no status route. */
function deriveStatus(cam: Camera): CameraStatus {
	const seen = cam.lastSeenAt ? Date.parse(cam.lastSeenAt) : NaN;
	return {
		id: cam.id ?? "", kind: cam.kind ?? "phone", name: cam.name, externalId: cam.externalId ?? null,
		state: cam.status === "online" ? "online" : cam.status === "offline" ? "offline" : "waiting",
		status: cam.status ?? "never", lastSeenAt: cam.lastSeenAt ?? null,
		secondsSinceSeen: Number.isNaN(seen) ? null : Math.max(0, Math.round((Date.now() - seen) / 1000)),
		watchCount: cam.watchCount ?? 0, hint: null, derived: true,
	};
}

class Cameras {
	constructor(private c: PerciaClient) {}
	list() { return unwrap(this.c.api.listCameras({})); }
	/** Returns `pairUrl`: a single-use link (10 minutes) a person opens on the phone that will be the camera. */
	/** Create a phone camera. `deviceKind` (phone, tablet or computer) only changes the wording shown to the person. */
	create(name: string, options: { deviceKind?: "phone" | "tablet" | "computer" } = {}) { return unwrap(this.c.api.createCamera({ body: { name, ...(options.deviceKind ? { deviceKind: options.deviceKind } : {}) } })); }
	/** A fresh pairing link; an unused earlier one stops working. */
	pair(id: string) { return unwrap(this.c.api.createCameraPairing({ path: { id } })); }
	delete(id: string) { return unwrap(this.c.api.deleteCamera({ path: { id } })); }

	/**
	 * Register a camera that a connector on a private network pushes to Percia (WHIP). Safe to call on every start:
	 * it is idempotent by `externalId`. The first call returns `token` (shown once: store it); later calls return the
	 * same camera with `token: null` and `existing: true` unless `onExisting` says otherwise.
	 */
	async registerPush(options: RegisterPushOptions): Promise<PushRegistration> {
		const res = (await unwrap(this.c.api.createCamera({ body: { name: options.name, kind: "push", externalId: options.externalId } }))) as PushResponse;
		return this.applyOnExisting(toRegistration(res), options.externalId, options.onExisting);
	}
	private async applyOnExisting(reg: PushRegistration, externalId: string, mode: RegisterPushOptions["onExisting"] = "return"): Promise<PushRegistration> {
		if (!reg.existing || reg.token) return reg;
		if (mode === "throw") throw new PerciaError(`Camera with externalId "${externalId}" already exists (${reg.camera.id}) and its token is shown only once. Use cameras.rotateToken("${reg.camera.id}") for a new one.`);
		if (mode === "rotate") {
			const rot = await this.rotateToken(reg.camera.id!);
			return { ...reg, token: rot.token ?? null, whipUrl: rot.whipUrl ?? reg.whipUrl, rotated: true };
		}
		return reg;
	}
	/** New publish token for a push camera, shown once; the old one stops working at once. Phone cameras answer 409 `wrong_kind`. Needs `cameras:write` and `watches:delete`. */
	rotateToken(id: string) { return unwrap(this.c.api.rotateCameraToken({ path: { id } })); }
	/** Stop accepting publishes for a push camera; the camera stays. `rotateToken` publishes again. Needs `cameras:write` and `watches:delete`. */
	revokeToken(id: string) { return unwrap(this.c.api.revokeCameraToken({ path: { id } })); }
	/**
	 * One camera's state from `GET /cameras/{id}/status`: `state` (`waiting` | `online` | `offline` | `revoked`), `status`
	 * (`online` = seen in the last 60 s, `offline`, `never`), `lastSeenAt`, `secondsSinceSeen`, `watchCount` and a `hint` that
	 * names the likely reason and the next step. Needs `cameras:read`.
	 *
	 * Older servers without that route answer 404: the SDK then reads `GET /cameras` instead and derives `state`
	 * (`derived: true`, `hint: null`, no `revoked`). A camera that is not yours is a `NotFoundError` either way.
	 */
	async status(id: string): Promise<CameraStatus> {
		try {
			return (await unwrap(this.c.api.getCameraStatus({ path: { id } }))) as CameraStatus;
		} catch (error) {
			if (!(error instanceof NotFoundError)) throw error;
			const found = (await this.list()).find((cam) => cam.id === id);
			if (!found) throw error;
			return deriveStatus(found);
		}
	}
	/**
	 * Register many push cameras (idempotent each) with `POST /cameras/bulk`: up to 10 per request, so longer lists are sent
	 * in chunks of 10. Each chunk is all or nothing against the camera limit (429 `camera_limit`, nothing created); that
	 * failure is reported on every item of that chunk and the next chunks still run. Results keep the input order.
	 * A server without the bulk route answers 404: the SDK then registers the items one by one with `registerPush`.
	 * Needs `cameras:write`; `externalId`s must be unique within a chunk.
	 */
	async bulk(items: BulkItem[], options: { concurrency?: number; onExisting?: RegisterPushOptions["onExisting"] } = {}): Promise<BulkResult[]> {
		const out: BulkResult[] = new Array(items.length);
		const finish = async (i: number, reg: PushRegistration) => {
			const item = items[i]!;
			try { out[i] = { externalId: item.externalId, ok: true, registration: await this.applyOnExisting(reg, item.externalId, options.onExisting) }; }
			catch (error) { out[i] = { externalId: item.externalId, ok: false, error }; }
		};
		const one = async (i: number) => {
			const item = items[i]!;
			try { out[i] = { externalId: item.externalId, ok: true, registration: await this.registerPush({ ...item, onExisting: options.onExisting }) }; }
			catch (error) { out[i] = { externalId: item.externalId, ok: false, error }; }
		};
		let legacy = false;
		for (let from = 0; from < items.length; from += BULK_MAX) {
			const idx = Array.from({ length: Math.min(BULK_MAX, items.length - from) }, (_, k) => from + k);
			if (!legacy) {
				try {
					const res = (await unwrap(this.c.api.createCameras({ body: { cameras: idx.map((i) => ({ name: items[i]!.name, externalId: items[i]!.externalId })) } }))) as { cameras?: PushResponse[] };
					const entries = res.cameras ?? [];
					for (const [k, i] of idx.entries()) {
						const entry = entries.find((e) => e.camera?.externalId === items[i]!.externalId) ?? entries[k];
						try { await finish(i, toRegistration(entry ?? {})); }
						catch (error) { out[i] = { externalId: items[i]!.externalId, ok: false, error }; }
					}
					continue;
				} catch (error) {
					if (!(error instanceof NotFoundError)) {
						for (const i of idx) out[i] = { externalId: items[i]!.externalId, ok: false, error };
						continue;
					}
					legacy = true; // no bulk route on this server (or phone cameras are off: registerPush then reports the 404 per item)
				}
			}
			let next = 0;
			const worker = async () => { for (let k = next++; k < idx.length; k = next++) await one(idx[k]!); };
			await Promise.all(Array.from({ length: Math.max(1, Math.min(options.concurrency ?? 3, idx.length)) }, worker));
		}
		return out;
	}
}

class Integrations {
	constructor(private c: PerciaClient) {}
	services() { return unwrap(this.c.api.listIntegrationServices({})); }
	list() { return unwrap(this.c.api.listIntegrations({})); }
	/** Start a connect link for a destination (Slack, Discord, Telegram, ...). Only a person can finish it; show `connectUrl` to them. */
	connect(body: Body<"createConnectLink">) { return unwrap(this.c.api.createConnectLink({ body })); }
	delete(id: string) { return unwrap(this.c.api.deleteIntegration({ path: { id } })); }
	watchRules(watchId: string) { return unwrap(this.c.api.listWatchIntegrations({ path: { id: watchId } })); }
	setWatchRules(watchId: string, body: Body<"setWatchIntegrations">) { return unwrap(this.c.api.setWatchIntegrations({ path: { id: watchId }, body })); }
}

class Hooks {
	constructor(private c: PerciaClient) {}
	list() { return unwrap(this.c.api.listHooks({})); }
	/** Subscribe an https address to signed deliveries. Needs the `hooks:write` scope. The response holds `secret` once. */
	create(body: Body<"createHook">) { return unwrap(this.c.api.createHook({ body })); }
	/** Idempotent: a hook that is already gone answers `{ ok: true, deleted: false }`. */
	delete(id: string) { return unwrap(this.c.api.deleteHook({ path: { id } })); }
	test(id: string) { return unwrap(this.c.api.testHook({ path: { id } })); }
}

class Account {
	constructor(private c: PerciaClient) {}
	/** The signed-in account. Session or OAuth token; API keys are refused by this route. */
	me() { return unwrap(this.c.api.getAccount({})); }
	/** Plan, free and credit minutes, how the account is charged and the next step. Read `canStartWatches` before creating a watch. */
	plan() { return unwrap(this.c.api.getPlan({})); }
	/** The same facts as the `billing` block of MCP `whoami`, from `plan()` (see `billingOf`). */
	async billing(): Promise<Billing> { return billingOf((await this.plan()) as Plan); }
	usage() { return unwrap(this.c.api.getUsage({})); }
}
