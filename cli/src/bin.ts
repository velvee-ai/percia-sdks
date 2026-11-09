#!/usr/bin/env node
import { spawn } from "node:child_process";
import { homedir } from "node:os";
import { createInterface } from "node:readline";
import { run } from "./program.js";
import type { Context } from "./context.js";

const ctl = new AbortController();
process.on("SIGINT", () => ctl.abort());
process.on("SIGTERM", () => ctl.abort());

function openUrl(url: string): Promise<boolean> {
	const [cmd, args] = process.platform === "darwin" ? ["open", [url]] : process.platform === "win32" ? ["cmd", ["/c", "start", "", url.replace(/&/g, "^&")]] : ["xdg-open", [url]];
	return new Promise((resolve) => {
		try {
			const child = spawn(cmd, args as string[], { stdio: "ignore", detached: true });
			child.on("error", () => resolve(false));
			child.on("spawn", () => (child.unref(), resolve(true)));
		} catch {
			resolve(false);
		}
	});
}

/** Hidden prompt on a TTY; one line from a pipe otherwise. */
function readSecret(prompt: string): Promise<string> {
	return new Promise((resolve, reject) => {
		if (!process.stdin.isTTY) {
			const rl = createInterface({ input: process.stdin });
			rl.once("line", (l) => (rl.close(), resolve(l)));
			rl.once("close", () => resolve(""));
			return;
		}
		process.stderr.write(prompt);
		let buf = "";
		process.stdin.setRawMode(true);
		process.stdin.resume();
		process.stdin.setEncoding("utf8");
		const onData = (ch: string) => {
			for (const c of ch) {
				if (c === "\r" || c === "\n") { done(); return resolve(buf); }
				if (c === "\u0003") { done(); return reject(new Error("Cancelled.")); }
				if (c === "\u007f" || c === "\b") buf = buf.slice(0, -1);
				else buf += c;
			}
		};
		const done = () => { process.stdin.setRawMode(false); process.stdin.pause(); process.stdin.off("data", onData); process.stderr.write("\n"); };
		process.stdin.on("data", onData);
	});
}

const ctx: Context = {
	argv0: "percia",
	stdout: (t) => void process.stdout.write(t),
	stderr: (t) => void process.stderr.write(t),
	env: process.env,
	platform: process.platform,
	cwd: process.cwd(),
	homedir: homedir(),
	isTTY: Boolean(process.stdin.isTTY && process.stdout.isTTY),
	fetch: (input, init) => fetch(input, init),
	now: () => Date.now(),
	sleep: (ms, signal) => new Promise<void>((resolve, reject) => {
		if (signal?.aborted) return reject(signal.reason);
		const t = setTimeout(resolve, ms);
		signal?.addEventListener("abort", () => (clearTimeout(t), reject(signal.reason)), { once: true });
	}),
	openUrl,
	readSecret,
	signal: ctl.signal,
};

// A closed pipe (`percia events list | head`) is not an error.
process.stdout.on("error", (e: NodeJS.ErrnoException) => { if (e.code === "EPIPE") process.exit(0); throw e; });
process.exitCode = await run(process.argv.slice(2), ctx);
