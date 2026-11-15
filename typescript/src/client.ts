import { createClient as createGeneratedClient, createConfig } from "./generated/client/index.js";
import type { Client } from "./generated/client/index.js";
import * as sdk from "./generated/sdk.gen.js";
import type { Camera, Event, EventPage, Watch } from "./generated/types.gen.js";
import { NotFoundError, PerciaError, errorFromResponse } from "./errors.js";
import type { BulkItem, BulkResult, PushRegistration } from "./push.js";
import { createRetryingFetch, type RetryOptions } from "./retry.js";
import { paginate } from "./pagination.js";

export const DEFAULT_BASE_URL = "https://playground.percia.ai";
export const SDK_VERSION = "0.2.0";

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
	/** Create a watch. The response is the only time `webhookSecret` is shown: store it. */
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

class Cameras {
	constructor(private c: PerciaClient) {}
	list() { return unwrap(this.c.api.listCameras({})); }
	/** Returns `pairUrl`: a single-use link (10 minutes) a person opens on the phone that will be the camera. */
	create(name: string) { return unwrap(this.c.api.createCamera({ body: { name } })); }
	/** A fresh pairing link; an unused earlier one stops working. */
	pair(id: string) { return unwrap(this.c.api.createCameraPairing({ path: { id } })); }
	delete(id: string) { return unwrap(this.c.api.deleteCamera({ path: { id } })); }

	/**
	 * Register a camera that a connector on a private network pushes to Percia (WHIP). Safe to call on every start:
	 * it is idempotent by `externalId`. The first call returns `token` (shown once: store it); later calls return the
	 * same camera with `token: null` and `existing: true` unless `onExisting` says otherwise.
	 */
	async registerPush(options: RegisterPushOptions): Promise<PushRegistration> {
		const res = (await unwrap(this.c.api.createCamera({ body: { name: options.name, kind: "push", externalId: options.externalId } }))) as { camera?: Camera; whipUrl?: string; token?: string | null; existing?: boolean; publish?: Record<string, unknown> };
		if (!res.camera?.id || !res.whipUrl) throw new PerciaError("Percia did not return a push camera (no id or whipUrl). Is the server new enough for kind: \"push\"?");
		const existing = res.existing === true;
		let reg: PushRegistration = { camera: res.camera, whipUrl: res.whipUrl, token: res.token ?? null, existing, rotated: false, publish: res.publish };
		if (existing && !reg.token) {
			const mode = options.onExisting ?? "return";
			if (mode === "throw") throw new PerciaError(`Camera with externalId "${options.externalId}" already exists (${res.camera.id}) and its token is shown only once. Use cameras.rotateToken("${res.camera.id}") for a new one.`);
			if (mode === "rotate") {
				const rot = await this.rotateToken(res.camera.id);
				reg = { ...reg, token: rot.token ?? null, whipUrl: rot.whipUrl ?? reg.whipUrl, rotated: true };
			}
		}
		return reg;
	}
	/** New publish token for a push camera, shown once; the old one stops working at once. Phone cameras answer 409 `wrong_kind`. Needs `cameras:write` and `watches:delete`. */
	rotateToken(id: string) { return unwrap(this.c.api.rotateCameraToken({ path: { id } })); }
	/** Stop accepting publishes for a push camera; the camera stays. `rotateToken` publishes again. Needs `cameras:write` and `watches:delete`. */
	revokeToken(id: string) { return unwrap(this.c.api.revokeCameraToken({ path: { id } })); }
	/**
	 * `id`, `name`, `kind`, `externalId`, `status` (`online` = seen in the last 60 s, `offline`, `never`), `lastSeenAt` and `watchCount`
	 * of one camera. The API has no per-camera status route; this reads the list, so it costs one request.
	 */
	async status(id: string) {
		const found = (await this.list()).find((c) => c.id === id);
		if (!found) throw new NotFoundError({ status: 404, code: "not_found", message: `No camera ${id} on this account.` });
		return found;
	}
	/**
	 * Register many push cameras (idempotent each). The API has no bulk route, so this runs `registerPush` with a small
	 * concurrency and reports each outcome: one failure (`camera_limit`, a bad id) does not stop the rest.
	 */
	async bulk(items: BulkItem[], options: { concurrency?: number; onExisting?: RegisterPushOptions["onExisting"] } = {}): Promise<BulkResult[]> {
		const out: BulkResult[] = new Array(items.length);
		let next = 0;
		const worker = async () => {
			for (let i = next++; i < items.length; i = next++) {
				const item = items[i]!;
				try { out[i] = { externalId: item.externalId, ok: true, registration: await this.registerPush({ ...item, onExisting: options.onExisting }) }; }
				catch (error) { out[i] = { externalId: item.externalId, ok: false, error }; }
			}
		};
		await Promise.all(Array.from({ length: Math.max(1, Math.min(options.concurrency ?? 3, items.length || 1)) }, worker));
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
	plan() { return unwrap(this.c.api.getPlan({})); }
	usage() { return unwrap(this.c.api.getUsage({})); }
}
