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

Emitted from percia-cf `ae63174` with `scripts/emit-from-cf.sh` (the live host is behind master) and pinned with `pnpm spec:sync --file ... --source "percia-cf ae63174"` (sha256 `63bbae07c77f...`, 110 operations) on 2026-11-16. New since the previous pin: the billing block on `GET /plan` (`label`, `freeMinutesLeft`, `creditMinutes`, `howCharged`, `nextStep`, `canStartWatches`, `bonusAvailable`, ...), `Camera.deviceKind`, goal understanding (`interpret`, `kind`, `concerns` on create, `interpretation` on a watch, `POST /watches/interpret`, `POST /watches/{id}/reinterpret`), `judging`, and the card replace routes. `pnpm spec:check` against the live host reports drift until percia-cf is deployed; re-pin from the live host then.
