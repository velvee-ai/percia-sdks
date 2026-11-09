#!/usr/bin/env bash
# Emit /api/openapi.json from a percia-cf checkout by running its own handler under vitest, without modifying that checkout.
# Usage: spec/scripts/emit-from-cf.sh /path/to/percia-cf   (then: pnpm spec:sync --file <printed path> --source "percia-cf <sha>")
set -euo pipefail
CF="${1:?path to percia-cf}"
OUT="${2:-$(mktemp -d)/openapi.json}"
WORK="$(mktemp -d)"
rsync -a --exclude node_modules --exclude .git --exclude .wrangler "$CF"/ "$WORK"/
ln -s "$CF/node_modules" "$WORK/node_modules"
cat > "$WORK/src/dump.test.ts" <<'TS'
import { test } from "vitest";
import { writeFileSync } from "node:fs";
import worker from "./index.ts";
test("dump", async () => {
	const res = await (worker as any).fetch(new Request("http://localhost/api/openapi.json"), {}, { waitUntil() {}, passThroughOnException() {} });
	writeFileSync(process.env.OUT!, await res.text());
});
TS
(cd "$WORK" && OUT="$OUT" npx vitest run src/dump.test.ts >/dev/null)
rm -rf "$WORK"
echo "$OUT"
