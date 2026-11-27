#!/usr/bin/env node
// Pull the Percia OpenAPI document and pin it.
//
//   node spec/scripts/sync.mjs                 fetch the live document, write spec/openapi.json + spec/spec.lock.json
//   node spec/scripts/sync.mjs --url <url>     fetch from another host (a staging or local worker)
//   node spec/scripts/sync.mjs --file <path>   pin a document from disk (for a document you saved locally)
//   node spec/scripts/sync.mjs --check         fetch the live document and exit 1 when its hash differs from the lock (CI drift check)
//   node spec/scripts/sync.mjs --verify-lock   offline: exit 1 when spec/openapi.json does not match spec/spec.lock.json
//
// The hash is over a canonical form (object keys sorted, 2-space indent) so key order from the server never causes drift.
import { createHash } from "node:crypto";
import { readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const root = join(dirname(fileURLToPath(import.meta.url)), "..");
const specPath = join(root, "openapi.json");
const lockPath = join(root, "spec.lock.json");
const DEFAULT_URL = "https://playground.percia.ai/api/openapi.json";

export const canonical = (value) => {
	const sort = (v) => (Array.isArray(v) ? v.map(sort) : v && typeof v === "object" ? Object.fromEntries(Object.keys(v).sort().map((k) => [k, sort(v[k])])) : v);
	return JSON.stringify(sort(value), null, 2) + "\n";
};
export const sha256 = (text) => createHash("sha256").update(text).digest("hex");

const args = process.argv.slice(2);
const flag = (name) => args.includes(name);
const opt = (name) => (args.includes(name) ? args[args.indexOf(name) + 1] : undefined);

const summarize = (doc) => {
	const operations = Object.values(doc.paths).flatMap((p) => Object.values(p).filter((o) => o && typeof o === "object" && o.operationId));
	return { openapi: doc.openapi, title: doc.info?.title, version: doc.info?.version, operations: operations.length, schemas: Object.keys(doc.components?.schemas ?? {}).length };
};

async function load(url) {
	const res = await fetch(url, { headers: { accept: "application/json", "user-agent": "percia-sdks-spec-sync" } });
	if (!res.ok) throw new Error(`GET ${url} answered ${res.status}`);
	return JSON.parse(await res.text());
}

if (flag("--verify-lock")) {
	const lock = JSON.parse(readFileSync(lockPath, "utf8"));
	const text = canonical(JSON.parse(readFileSync(specPath, "utf8")));
	if (sha256(text) !== lock.sha256) {
		console.error(`spec/openapi.json (${sha256(text).slice(0, 12)}) does not match spec.lock.json (${lock.sha256.slice(0, 12)}). Run: pnpm spec:sync`);
		process.exit(1);
	}
	if (text !== readFileSync(specPath, "utf8")) {
		console.error("spec/openapi.json is not in canonical form. Run: pnpm spec:sync --file spec/openapi.json");
		process.exit(1);
	}
	console.log(`spec ok: sha256 ${lock.sha256.slice(0, 12)}, ${lock.operations} operations`);
} else if (flag("--check")) {
	const lock = JSON.parse(readFileSync(lockPath, "utf8"));
	const url = opt("--url") ?? lock.checkUrl ?? DEFAULT_URL;
	const live = canonical(await load(url));
	if (sha256(live) !== lock.sha256) {
		const s = summarize(JSON.parse(live));
		console.error(`SPEC DRIFT: ${url} is ${sha256(live).slice(0, 12)} (${s.operations} operations), the pinned spec is ${lock.sha256.slice(0, 12)} (${lock.operations} operations, from ${lock.source}).`);
		console.error("Review the change, then run: pnpm spec:sync && pnpm generate, and commit the result.");
		process.exit(1);
	}
	console.log(`no drift: ${url} matches ${lock.sha256.slice(0, 12)}`);
} else {
	const file = opt("--file");
	const url = opt("--url") ?? DEFAULT_URL;
	const doc = file ? JSON.parse(readFileSync(file, "utf8")) : await load(url);
	const text = canonical(doc);
	writeFileSync(specPath, text);
	const prev = (() => { try { return JSON.parse(readFileSync(lockPath, "utf8")); } catch { return {}; } })();
	const lock = {
		source: file ? (opt("--source") ?? `file:${file}`) : url,
		checkUrl: opt("--check-url") ?? prev.checkUrl ?? DEFAULT_URL,
		sha256: sha256(text),
		...summarize(doc),
		note: opt("--note") ?? (file ? prev.note : undefined),
	};
	writeFileSync(lockPath, JSON.stringify(lock, (k, v) => (v === undefined ? undefined : v), 2) + "\n");
	console.log(`pinned ${lock.title} ${lock.version}: ${lock.operations} operations, sha256 ${lock.sha256.slice(0, 12)}`);
}
