import { createClient as createGeneratedClient, createConfig } from "./generated/client/index.js";
import type { Client } from "./generated/client/index.js";
import * as sdk from "./generated/sdk.gen.js";
import type { Event, EventPage, Watch } from "./generated/types.gen.js";
import { PerciaError, errorFromResponse } from "./errors.js";
import { createRetryingFetch, type RetryOptions } from "./retry.js";
import { paginate } from "./pagination.js";

export const DEFAULT_BASE_URL = "https://playground.percia.ai";
export const SDK_VERSION = "0.1.0";

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

class Cameras {
	constructor(private c: PerciaClient) {}
	list() { return unwrap(this.c.api.listCameras({})); }
	/** Returns `pairUrl`: a single-use link (10 minutes) a person opens on the phone that will be the camera. */
	create(name: string) { return unwrap(this.c.api.createCamera({ body: { name } })); }
	/** A fresh pairing link; an unused earlier one stops working. */
	pair(id: string) { return unwrap(this.c.api.createCameraPairing({ path: { id } })); }
	delete(id: string) { return unwrap(this.c.api.deleteCamera({ path: { id } })); }
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
