import { readdirSync, readFileSync, statSync } from "node:fs";
import { join } from "node:path";
import { expect, it } from "vitest";

// The core must run on edge runtimes (Workers, Deno, Bun, browsers): fetch + Web Crypto only, no Node-only APIs.
const files = (dir: string): string[] => readdirSync(dir).flatMap((f) => (statSync(join(dir, f)).isDirectory() ? files(join(dir, f)) : f.endsWith(".ts") ? [join(dir, f)] : []));

it("src has no Node-only imports or globals", () => {
	const banned = /from\s+["']node:|require\(|\bprocess\.|\bBuffer\b|from\s+["'](fs|path|crypto|http|https|os|stream)["']/;
	const offenders = files(new URL("../src", import.meta.url).pathname).filter((f) => banned.test(readFileSync(f, "utf8")));
	expect(offenders).toEqual([]);
});
