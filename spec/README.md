# spec

The single source of truth for every SDK, the CLI, the Postman collection and the examples: the Percia OpenAPI 3.1 document.

| File | |
|---|---|
| `openapi.json` | The pinned document, in canonical form (sorted keys). **Committed.** |
| `spec.lock.json` | Where it came from, its sha256, operation count. |
| `webhook-vectors.json` | Shared signature test cases (copied from percia-cf `sdk/vectors.json`), used by the TS, Python and example verifiers. |
| `camera-push-contract.json` | The camera push contract recorded from the percia-cf spec (fake tokens), shared by the TS, Python and CLI tests and the examples. |
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

Pinned from the live host `https://playground.percia.ai/api/openapi.json` (sha256 `ed96ffa14960...`, 105 operations) on 2026-11-14, after percia-cf master `bb95c92` was deployed (Worker versions `d7aff9a6`, then `5a591ed8`). It includes the camera push routes (`POST /cameras` with `kind: "push"`, `POST /cameras/bulk`, `GET /cameras/{id}/status`, `POST|DELETE /cameras/{id}/token`), the `/cam/claim` body, SMS/WhatsApp, `GET /events`, `/hooks`, and the credits and billing routes. `pnpm spec:check` passes (no drift). The earlier draft addition (push routes taken from an unmerged branch) is gone: nothing in the pin is hand-merged. `scripts/emit-from-cf.sh` remains for the case where the live host is behind a percia-cf checkout; `pnpm spec:sync --file <path> --source "..."` pins its output.
