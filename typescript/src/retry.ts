import { PerciaConnectionError, PerciaTimeoutError, parseRetryAfter } from "./errors.js";

export type RetryOptions = {
	/** Retries after the first attempt. Default 2. 0 disables retrying. */
	maxRetries?: number;
	/** First backoff delay. Default 500 ms; doubles each attempt with full jitter. */
	baseDelayMs?: number;
	/** Cap for one backoff delay. Default 8000 ms. */
	maxDelayMs?: number;
	/** A Retry-After larger than this is not waited for: the response is returned as is. Default 60000 ms. */
	maxRetryAfterMs?: number;
	/** Per-attempt timeout. Default 30000 ms; 0 disables. */
	timeoutMs?: number;
	/** Also retry non-idempotent requests (POST, PATCH) on 5xx and network errors. Default false: a create that returned 5xx may have created the resource. 429 is always retried. */
	retryNonIdempotent?: boolean;
	/** Injected for tests. */
	sleep?: (ms: number, signal?: AbortSignal | null) => Promise<void>;
	random?: () => number;
};

const IDEMPOTENT = new Set(["GET", "HEAD", "PUT", "DELETE", "OPTIONS"]);
const RETRYABLE_5XX = new Set([500, 502, 503, 504]);

export const defaultSleep = (ms: number, signal?: AbortSignal | null) =>
	new Promise<void>((resolve, reject) => {
		if (signal?.aborted) return reject(signal.reason);
		const t = setTimeout(() => (signal?.removeEventListener("abort", onAbort), resolve()), ms);
		const onAbort = () => (clearTimeout(t), reject(signal!.reason));
		signal?.addEventListener("abort", onAbort, { once: true });
	});

/** Delay before retry number `attempt` (1-based): exponential with full jitter, or the server's Retry-After when it sent one. */
export function backoffMs(attempt: number, o: Required<Pick<RetryOptions, "baseDelayMs" | "maxDelayMs" | "random">>, retryAfterMs?: number): number {
	if (retryAfterMs !== undefined) return retryAfterMs;
	const ceiling = Math.min(o.maxDelayMs, o.baseDelayMs * 2 ** (attempt - 1));
	return Math.round(o.random() * ceiling);
}

/** Merge the caller's AbortSignal with a per-attempt timeout without AbortSignal.any (older edge runtimes lack it). */
function withTimeout(signal: AbortSignal | null | undefined, ms: number): { signal: AbortSignal | undefined; cleanup: () => void; timedOut: () => boolean } {
	if (!ms && !signal) return { signal: undefined, cleanup: () => {}, timedOut: () => false };
	const ctl = new AbortController();
	let timedOut = false;
	const onAbort = () => ctl.abort(signal!.reason);
	if (signal) signal.aborted ? ctl.abort(signal.reason) : signal.addEventListener("abort", onAbort, { once: true });
	const timer = ms ? setTimeout(() => ((timedOut = true), ctl.abort(new PerciaTimeoutError(`Request timed out after ${ms} ms`))), ms) : undefined;
	return { signal: ctl.signal, cleanup: () => (clearTimeout(timer), signal?.removeEventListener("abort", onAbort)), timedOut: () => timedOut };
}

/**
 * Wrap `fetch` with retries, a per-attempt timeout and a header hook. Takes and returns the standard fetch shape, so it works on
 * Node 20+, Workers, Deno, Bun and browsers. The generated client calls `fetch(request)` with a Request; that is cloned per attempt.
 */
export function createRetryingFetch(base: typeof fetch, opts: RetryOptions & { prepare?: (req: Request) => Request | Promise<Request> } = {}): typeof fetch {
	const maxRetries = opts.maxRetries ?? 2;
	const baseDelayMs = opts.baseDelayMs ?? 500;
	const maxDelayMs = opts.maxDelayMs ?? 8000;
	const maxRetryAfterMs = opts.maxRetryAfterMs ?? 60_000;
	const timeoutMs = opts.timeoutMs ?? 30_000;
	const sleep = opts.sleep ?? defaultSleep;
	const random = opts.random ?? Math.random;

	return async (input: RequestInfo | URL, init?: RequestInit): Promise<Response> => {
		const original = new Request(input as RequestInfo, init);
		const method = original.method.toUpperCase();
		const idempotent = IDEMPOTENT.has(method) || original.headers.has("idempotency-key") || opts.retryNonIdempotent === true;
		const callerSignal = original.signal;

		for (let attempt = 0; ; attempt++) {
			if (callerSignal.aborted) throw callerSignal.reason;
			let req = original.clone();
			if (opts.prepare) req = await opts.prepare(req);
			const t = withTimeout(callerSignal, timeoutMs);
			let response: Response | undefined;
			let failure: unknown;
			try {
				response = await base(t.signal ? new Request(req, { signal: t.signal }) : req);
			} catch (e) {
				failure = e;
			} finally {
				t.cleanup();
			}

			if (response) {
				const status = response.status;
				const retriable = status === 429 || (idempotent && RETRYABLE_5XX.has(status));
				if (!retriable || attempt >= maxRetries) return response;
				const retryAfter = parseRetryAfter(response.headers.get("retry-after"));
				if (retryAfter !== undefined && retryAfter > maxRetryAfterMs) return response;
				await response.body?.cancel().catch(() => {});
				await sleep(backoffMs(attempt + 1, { baseDelayMs, maxDelayMs, random }, retryAfter), callerSignal);
				continue;
			}

			// No response. The caller's own abort is never retried or wrapped.
			if (callerSignal.aborted) throw failure;
			const timeout = t.timedOut();
			const err = timeout ? new PerciaTimeoutError(`Request timed out after ${timeoutMs} ms`, { cause: failure }) : new PerciaConnectionError(`Could not reach Percia: ${failure instanceof Error ? failure.message : String(failure)}`, { cause: failure });
			if (!idempotent || attempt >= maxRetries) throw err;
			await sleep(backoffMs(attempt + 1, { baseDelayMs, maxDelayMs, random }), callerSignal);
		}
	};
}
