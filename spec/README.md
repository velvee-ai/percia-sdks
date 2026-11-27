# spec

The single source of truth for every SDK, the CLI, the Postman collection and the examples: the Percia OpenAPI 3.1 document.

| File | |
|---|---|
| `openapi.json` | The pinned document, in canonical form (sorted keys). **Committed.** |
| `spec.lock.json` | Where it came from, its sha256, operation count. |
| `webhook-vectors.json` | Shared signature test cases (fake secrets), used by the TS, Python and example verifiers. |
| `camera-push-contract.json` | The camera push contract recorded from the Percia API (fake tokens), shared by the TS, Python and CLI tests and the examples. |
| `redocly.yaml` | Lint rules (`pnpm spec:lint`). |
| `scripts/sync.mjs` | Fetch and pin (`pnpm spec:sync`), drift check (`pnpm spec:check`), offline integrity check (`pnpm spec:verify`). |

```bash
pnpm spec:sync                      # pin https://playground.percia.ai/api/openapi.json
pnpm spec:sync --url https://staging.example/api/openapi.json
pnpm spec:check                     # exit 1 when the live document differs from the pin (CI: spec-drift.yml)
pnpm generate                       # regenerate TS, Python and Postman from the pin; commit the diff
```

## Current pin

Pinned from https://playground.percia.ai/api/openapi.json (Percia API 1.0.0, 146 operations; sha256 in `spec.lock.json`). `pnpm spec:check` fails when the live document differs: re-pin with `pnpm spec:sync && pnpm generate` and commit the result.
