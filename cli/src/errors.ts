import { PerciaApiError, PerciaConnectionError, PerciaError } from "@percia/sdk";

/** Documented exit codes. */
export const EXIT = { OK: 0, FAILURE: 1, USAGE: 2, AUTH: 3, NOT_FOUND: 4, LIMIT: 5, NETWORK: 6, SERVER: 7 } as const;

/** An error the CLI wants to print as is, with its exit code. */
export class CliError extends Error {
	constructor(message: string, readonly exitCode: number = EXIT.FAILURE, readonly hint?: string) {
		super(message);
		this.name = "CliError";
	}
}

export function exitCodeFor(e: unknown): number {
	if (e instanceof CliError) return e.exitCode;
	if (e instanceof PerciaApiError) {
		if (e.status === 401 || e.status === 403) return EXIT.AUTH;
		if (e.status === 404) return EXIT.NOT_FOUND;
		if (e.status === 400) return EXIT.USAGE;
		if (e.status === 409 || e.status === 429) return EXIT.LIMIT;
		if (e.status >= 500) return EXIT.SERVER;
		return EXIT.FAILURE;
	}
	if (e instanceof PerciaConnectionError) return EXIT.NETWORK;
	return EXIT.FAILURE;
}

/** Human message plus an actionable hint; never includes credentials. */
export function describeError(e: unknown): { message: string; hint?: string; details: Record<string, unknown> } {
	if (e instanceof PerciaApiError) {
		let hint: string | undefined;
		if (e.status === 401) hint = "Run `percia login`, or set PERCIA_API_KEY.";
		else if (e.status === 403 && e.code === "insufficient_scope") hint = "The credential lacks a scope. Create a key with it, or run `percia login --scopes ...`.";
		else if (e.status === 429 && e.retryAfterSec) hint = `Retry in ${Math.ceil(e.retryAfterSec)}s.`;
		return { message: stripControl(e.message), hint, details: { status: e.status, code: e.code, field: e.field, request_id: e.requestId } };
	}
	if (e instanceof CliError) return { message: e.message, hint: e.hint, details: {} };
	if (e instanceof PerciaError) return { message: e.message, details: {} };
	return { message: e instanceof Error ? e.message : String(e), details: {} };
}

/** Untrusted text (event reasons, labels, error messages) must not carry terminal escape sequences. */
export function stripControl(s: unknown): string {
	// eslint-disable-next-line no-control-regex
	return String(s ?? "").replace(/[\u0000-\u0008\u000b-\u001f\u007f-\u009f]/g, "");
}
