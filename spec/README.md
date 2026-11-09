# spec

The single source of truth for every SDK, the CLI, the Postman collection and the examples: the Percia OpenAPI 3.1 document.

| File | |
|---|---|
| `openapi.json` | The pinned document, in canonical form (sorted keys). **Committed.** |
| `spec.lock.json` | Where it came from, its sha256, operation count. |
| `webhook-vectors.json` | Shared signature test cases (copied from percia-cf `sdk/vectors.json`), used by the TS, Python and example verifiers. |
| `redocly.yaml` | Lint rules (`pnpm spec:lint`). |
| `scripts/sync.mjs` | Fetch and pin (`pnpm spec:sync`), drift check (`pnpm spec:check`), offline integrity check (`pnpm spec:verify`). |
| `scripts/emit-from-cf.sh` | Emit the document from a percia-cf checkout when the live host is behind. |

```bash
pnpm spec:sync                      # pin https://playground.percia.ai/api/openapi.json
pnpm spec:sync --url https://staging.example/api/openapi.json
pnpm spec:check                     # exit 1 when the live document differs from the pin (CI: spec-drift.yml)
pnpm generate                       # regenerate TS, Python and Postman from the pin; commit the diff
```

## Current pin

The live host `playground.percia.ai` serves an older build than percia-cf master: it lacks `GET /api/events`, `GET /api/events/sample`, the `/api/hooks` routes and `getStatus`, and names operations mechanically (`postWatchesOwned`). The pin is therefore the document emitted by percia-cf master (`e8b1cc6`), which has descriptive `operationId`s (`createWatch`, `listAccountEvents`, `createHook`...). Until master is deployed, `pnpm spec:check` correctly reports drift. After the deploy: `pnpm spec:sync`, `pnpm generate`, commit.
