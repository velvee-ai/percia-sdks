# Changelog

## 0.3.0 (unreleased)

- `events.stream({ watchId, concernId, type, backlog, since, signal, maxReconnects, idleTimeoutMs })`: async iterator over the developer event feed (`GET /api/events/stream`, SSE, fetch streaming). Yields `open`, `event` (with `cursor`, the parsed `event` and the exact `data` string), `resync`, `end`, `reconnect`, `ping`. Reconnects with `Last-Event-ID`, exponential backoff with jitter, `Retry-After` on 429, an idle timeout, dedupe on `eventId`; throws typed errors for 401/403/404/400; ends without an error when `signal` aborts. Also exported: `streamEvents`, `parseSse` and the types `EventStreamOptions`, `StreamItem`, `StreamedEvent`. `verifyWebhookSignature` and `signWebhook` are unchanged.
- Billing and goal understanding (additive, optional in types): `account.billing()` returns the `billing` block of MCP `whoami` from `GET /api/plan`; new `billingOf(plan)`, `describeBilling(billing)` and the types `Plan`, `Billing`, `Concern`, `Interpretation`. `account.plan()` now has every billing field in its type (`label`, `freeMinutesLeft`, `creditMinutes`, `howCharged`, `nextStep`, `canStartWatches`, `blockReason`, `bonusAvailable`, ...).
- `watches.create` accepts `interpret: false`, `kind` and `concerns`; `watches.interpret(goal)` and `watches.reinterpret(id)`; a watch carries `interpretation`.
- `cameras.create(name, { deviceKind })`; `Camera.deviceKind` is `phone | tablet | computer | null`.
- Regenerated from the spec pinned at percia-cf `ae63174` (110 operations).
- `SDK_VERSION` is 0.3.0.

## 0.2.0 (unreleased)

- Camera push (cameras on a private network): `cameras.registerPush({ name, externalId })` (idempotent; returns `whipUrl` and the one-time `token`, or `existing: true, token: null`; `onExisting: "return" | "rotate" | "throw"`), `cameras.rotateToken`, `cameras.revokeToken`, `cameras.status`, `cameras.bulk`.
- Helpers that never carry the token: `buildPublishCommands` (ffmpeg, OBS, GStreamer, heartbeat), `publishArgv` (for spawning), `redactRegistration`, `scrubToken`.
- `cameras.status(id)` calls `GET /cameras/{id}/status` and returns `state` (`waiting | online | offline | revoked`), `status`, `lastSeenAt`, `secondsSinceSeen`, `watchCount`, `hint` (new `CameraStatus` type). On a 404 (older server) it reads `GET /cameras` and derives the state (`derived: true`).
- `cameras.bulk(items, { onExisting })` calls `POST /cameras/bulk`, 10 per request (longer lists are chunked), results per item in input order; a 404 falls back to one `registerPush` per item. The `concurrency` option only applies to that fallback.
- Regenerated from the live spec (105 operations): token routes, `kind`, `externalId`, status, bulk, `/cam/claim` body, credits and billing routes.

## 0.1.0 (unreleased)

- First release. Typed client generated from the Percia OpenAPI document with `@hey-api/openapi-ts`; hand-written layer for auth, retries, typed errors, cursor pagination and webhook signature verification.
