import type { PerciaClient } from "@percia/sdk";

/** Everything the commands touch outside their own logic, injectable so tests run offline with no real terminal, browser or home directory. */
export type Context = {
	argv0: string;
	stdout: (text: string) => void;
	stderr: (text: string) => void;
	env: Record<string, string | undefined>;
	platform: NodeJS.Platform;
	cwd: string;
	homedir: string;
	isTTY: boolean;
	fetch: typeof fetch;
	now: () => number;
	sleep: (ms: number, signal?: AbortSignal) => Promise<void>;
	/** Open a URL in the user's browser. Returns false when it could not. */
	openUrl: (url: string) => Promise<boolean>;
	/** Read a secret without echo (TTY) or one line from stdin (pipe). */
	readSecret: (prompt: string) => Promise<string>;
	/** Run a program to completion and capture its output; `undefined` when it cannot be started (not installed). */
	capture: (cmd: string, args: string[]) => Promise<{ code: number | null; stdout: string; stderr: string } | undefined>;
	/** Run a long-lived program in the foreground (stdin closed), streaming its stderr. Resolves with the exit code (null when killed by `signal`). */
	exec: (cmd: string, args: string[], opts: { signal?: AbortSignal; onStderr?: (chunk: string) => void }) => Promise<{ code: number | null; startError?: string }>;
	/** Set by the run loop on SIGINT so follow/listen loops stop cleanly. */
	signal: AbortSignal;
};

export type GlobalOptions = { json?: boolean; baseUrl?: string; quiet?: boolean };

export type Session = { client: PerciaClient; baseUrl: string; auth: "api_key" | "oauth"; source: "env" | "config" };
