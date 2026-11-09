/** Every error the SDK throws extends PerciaError, so `catch (e) { if (e instanceof PerciaError) ... }` is enough. */
export class PerciaError extends Error {
	constructor(message: string, options?: { cause?: unknown }) {
		super(message, options);
		this.name = new.target.name;
	}
}

/** Stable machine-readable codes from the shared error envelope (`error.code`). Unknown codes pass through as strings. */
export type PerciaErrorCode = string;

export type ApiErrorInit = {
	status: number;
	code?: PerciaErrorCode;
	message: string;
	field?: string;
	requestId?: string;
	retryAfterSec?: number;
	body?: unknown;
	headers?: Headers;
};

/** The API answered with a non-2xx status. Branch on `status` and `code`, never on `message`. */
export class PerciaApiError extends PerciaError {
	readonly status: number;
	/** `error.code` from the envelope, e.g. `insufficient_scope`, `plan_limit`, `not_found`. */
	readonly code: PerciaErrorCode | undefined;
	/** Name of the first invalid request field, on validation failures. */
	readonly field: string | undefined;
	/** The `x-percia-request-id` of the failed request. Quote it when reporting a problem. */
	readonly requestId: string | undefined;
	/** Seconds from the `Retry-After` header, when the server sent one. */
	readonly retryAfterSec: number | undefined;
	readonly body: unknown;
	readonly headers: Headers | undefined;

	constructor(init: ApiErrorInit) {
		super(init.requestId ? `${init.message} (${init.status}${init.code ? ` ${init.code}` : ""}, request ${init.requestId})` : init.message);
		this.status = init.status;
		this.code = init.code;
		this.field = init.field;
		this.requestId = init.requestId;
		this.retryAfterSec = init.retryAfterSec;
		this.body = init.body;
		this.headers = init.headers;
	}
}

/** 401: missing, expired or revoked credential. */
export class AuthenticationError extends PerciaApiError {}
/** 403: the credential lacks a scope (`code: "insufficient_scope"`, see `requiredScope`) or the resource is another account's. */
export class PermissionError extends PerciaApiError {
	/** The scope the message names, when it is an `insufficient_scope` error. */
	get requiredScope(): string | undefined {
		return /\b([a-z]+:[a-z]+)\b/.exec(this.message)?.[1];
	}
}
/** 404: no such resource, or it is not yours (the two look the same on purpose). */
export class NotFoundError extends PerciaApiError {}
/** 400: a field failed validation (`field` names it) or the request is not allowed (`goal_not_allowed`, ...). */
export class ValidationError extends PerciaApiError {}
/** 409: state conflict (`camera_in_use`, `agent_in_use`, `nothing_to_publish`). */
export class ConflictError extends PerciaApiError {}
/** 429: rate limited or a plan/count limit (`plan_limit`, `camera_limit`, ...). The SDK already retried rate limits; `retryAfterSec` is the server's hint. */
export class RateLimitError extends PerciaApiError {}
/** 5xx. */
export class ServerError extends PerciaApiError {}

/** No HTTP response: DNS, TLS, connection reset or a timeout. */
export class PerciaConnectionError extends PerciaError {}
export class PerciaTimeoutError extends PerciaConnectionError {}

export type WebhookSignatureErrorCode = "malformed" | "stale_timestamp" | "mismatch";
/** A webhook delivery failed verification. `code` matches the shared test vectors. */
export class WebhookSignatureError extends PerciaError {
	readonly code: WebhookSignatureErrorCode;
	constructor(code: WebhookSignatureErrorCode, message?: string) {
		super(message ?? `Invalid Percia-Signature: ${code}`);
		this.code = code;
	}
}

/** Build the most specific error class for a failed response. `body` is the parsed JSON (or text). */
export function errorFromResponse(response: Response, body: unknown): PerciaApiError {
	const env = (body && typeof body === "object" ? body : {}) as { error?: { code?: string; message?: string; field?: string; request_id?: string }; message?: string; request_id?: string };
	const status = response.status;
	const retryAfter = parseRetryAfter(response.headers.get("retry-after"));
	const init: ApiErrorInit = {
		status,
		code: env.error?.code,
		message: env.error?.message ?? env.message ?? (typeof body === "string" && body ? body.slice(0, 200) : `HTTP ${status}`),
		field: env.error?.field,
		requestId: env.error?.request_id ?? env.request_id ?? response.headers.get("x-percia-request-id") ?? undefined,
		retryAfterSec: retryAfter === undefined ? undefined : retryAfter / 1000,
		body,
		headers: response.headers,
	};
	if (status === 401) return new AuthenticationError(init);
	if (status === 403) return new PermissionError(init);
	if (status === 404) return new NotFoundError(init);
	if (status === 400) return new ValidationError(init);
	if (status === 409) return new ConflictError(init);
	if (status === 429) return new RateLimitError(init);
	if (status >= 500) return new ServerError(init);
	return new PerciaApiError(init);
}

/** Milliseconds from a `Retry-After` header (delta-seconds or an HTTP date); undefined when absent or unparseable. */
export function parseRetryAfter(value: string | null | undefined, now: number = Date.now()): number | undefined {
	if (!value) return undefined;
	const v = value.trim();
	if (/^\d+(\.\d+)?$/.test(v)) return Math.round(Number(v) * 1000);
	const at = Date.parse(v);
	return Number.isNaN(at) ? undefined : Math.max(0, at - now);
}
