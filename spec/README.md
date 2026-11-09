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

Pinned from the live host `https://playground.percia.ai/api/openapi.json` (sha256 `72818549339f...`, 96 operations), which matched percia-cf master `2a65ab8` on 2026-11-09 (it includes `GET /api/events`, the `/api/hooks` routes and Twilio SMS/WhatsApp). While the work was being built the live host briefly served an older build; `scripts/emit-from-cf.sh` emits the document from a percia-cf checkout for that situation, and `pnpm spec:sync --file <path> --source "..."` pins it.
