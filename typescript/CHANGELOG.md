# Changelog

## 0.3.5 (2026-11-27)

- Synced with the Percia API (146 operations). Deploying a published agent to a watch (`agentId`, `agentVersion`) works again: its concerns are what the watch judges, and a version a watch cannot run answers 422 `agent_deploy_unavailable`, also from `POST /api/agents/{id}/publish` when a watch follows the latest. Create can answer 400 `agent_not_published`. Redeeming a used-up code answers 409 `code_fully_claimed` (new error code). `SDK_VERSION` is 0.3.5.

## 0.3.4 (2026-11-27)

- Synced with the Percia API (146 operations). `PATCH /api/watches/{id}` takes `acknowledgeUnsupported`; a new `goal` is read by Percia before anything changes, so the update can fail with 409 `unsupported_not_acknowledged`, 422 `clarification_needed` / `draft_refused` / `draft_multi_watch`, 429 `rate_limited` or 503 `layer_*`, and then nothing changes. Deploying an agent to a watch (`agentId`, `agentVersion`) is switched off: 422 `agent_deploy_unavailable` (new error code). `SDK_VERSION` is 0.3.4.

## 0.3.3 (2026-11-27)

- Synced with the Percia API (146 operations): new `GET /api/whoami` (`getWhoami`), which any valid API key, OAuth access token or session passes; OAuth descriptions and the `judging` state text updated. New `client.account.whoami()` and the type `Whoami`. `SDK_VERSION` is 0.3.3.

## 0.3.2 (2026-11-27)

- Synced with the Percia API after the Percia 2.0-only cleanup (145 operations). Removed from the generated models: `interpret`, `concerns`, `acknowledge`, `interpretation` and `runtime: "core"` on create and update watch (the API refuses them with 422 `invalid_request`; a goal is read by Percia's layer and an unclear one answers 422 `clarification_needed`, answered through the draft routes), `ephemeral` and `expiresAt` on watch reads, and the emailed-manage-link operation `getManagedWatch` (`GET /api/manage/{token}`, now 404). Request and response summaries match the live API text. `SDK_VERSION` is 0.3.2.

## 0.3.1 (2026-11-27)

- Package metadata only (no API or behaviour change): author Velvee, Inc. <support@velvee.ai>, homepage https://www.percia.ai, repository, bugs, license MIT. `SDK_VERSION` is 0.3.1.

## 0.3.0 (2026-11-27)

- `events.stream({ watchId, concernId, type, backlog, since, signal, maxReconnects, idleTimeoutMs })`: async iterator over the developer event feed (`GET /api/events/stream`, SSE, fetch streaming). Yields `open`, `event` (with `cursor`, the parsed `event` and the exact `data` string), `resync`, `end`, `reconnect`, `ping`. Reconnects with `Last-Event-ID`, exponential backoff with jitter, `Retry-After` on 429, an idle timeout, dedupe on `eventId`; throws typed errors for 401/403/404/400; ends without an error when `signal` aborts. Also exported: `streamEvents`, `parseSse` and the types `EventStreamOptions`, `StreamItem`, `StreamedEvent`. `verifyWebhookSignature` and `signWebhook` are unchanged.
- Billing (additive, optional in types): `account.billing()` returns the `billing` block of MCP `whoami` from `GET /api/plan`; new `billingOf(plan)`, `describeBilling(billing)` and the types `Plan`, `Billing`. `account.plan()` now has every billing field in its type (`label`, `freeMinutesLeft`, `creditMinutes`, `howCharged`, `nextStep`, `canStartWatches`, `blockReason`, `bonusAvailable`, ...).
- `cameras.create(name, { deviceKind })`; `Camera.deviceKind` is `phone | tablet | computer | null`.
- Regenerated from the current Percia API spec (146 operations).
- `SDK_VERSION` is 0.3.0.

## 0.2.0 (unreleased)

- Camera push (cameras on a private network): `cameras.registerPush({ name, externalId })` (idempotent; returns `whipUrl` and the one-time `token`, or `existing: true, token: null`; `onExisting: "return" | "rotate" | "throw"`), `cameras.rotateToken`, `cameras.revokeToken`, `cameras.status`, `cameras.bulk`.
- Helpers that never carry the token: `buildPublishCommands` (ffmpeg, OBS, GStreamer, heartbeat), `publishArgv` (for spawning), `redactRegistration`, `scrubToken`.
- `cameras.status(id)` calls `GET /cameras/{id}/status` and returns `state` (`waiting | online | offline | revoked`), `status`, `lastSeenAt`, `secondsSinceSeen`, `watchCount`, `hint` (new `CameraStatus` type). On a 404 (older server) it reads `GET /cameras` and derives the state (`derived: true`).
- `cameras.bulk(items, { onExisting })` calls `POST /cameras/bulk`, 10 per request (longer lists are chunked), results per item in input order; a 404 falls back to one `registerPush` per item. The `concurrency` option only applies to that fallback.
- Regenerated from the live spec (105 operations): token routes, `kind`, `externalId`, status, bulk, `/cam/claim` body, credits and billing routes.

## 0.1.0 (unreleased)

- First release. Typed client generated from the Percia OpenAPI document with `@hey-api/openapi-ts`; hand-written layer for auth, retries, typed errors, cursor pagination and webhook signature verification.
