# Changelog

## 0.3.5 (2026-11-27)

- Synced with the Percia API (146 operations). Deploying a published agent to a watch (`agentId`, `agentVersion`) works again: its concerns are what the watch judges, and a version a watch cannot run answers 422 `agent_deploy_unavailable`, also from `POST /api/agents/{id}/publish` when a watch follows the latest. Create can answer 400 `agent_not_published`. Redeeming a used-up code answers 409 `code_fully_claimed` (new error code).

## 0.3.4 (2026-11-27)

- Synced with the Percia API (146 operations). `PATCH /api/watches/{id}` takes `acknowledgeUnsupported`; a new `goal` is read by Percia before anything changes, so the update can fail with 409 `unsupported_not_acknowledged`, 422 `clarification_needed` / `draft_refused` / `draft_multi_watch`, 429 `rate_limited` or 503 `layer_*`, and then nothing changes. Deploying an agent to a watch (`agentId`, `agentVersion`) is switched off: 422 `agent_deploy_unavailable` (new error code).

## 0.3.3 (2026-11-27)

- Synced with the Percia API (146 operations): new `GET /api/whoami` (`getWhoami`), which any valid API key, OAuth access token or session passes; OAuth descriptions and the `judging` state text updated. New `client.account.whoami()` (sync and `AsyncPercia`).

## 0.3.2 (2026-11-27)

- Synced with the Percia API after the Percia 2.0-only cleanup (145 operations). Removed from the generated models: `interpret`, `concerns`, `acknowledge`, `interpretation` and `runtime: "core"` on create and update watch (the API refuses them with 422 `invalid_request`; a goal is read by Percia's layer and an unclear one answers 422 `clarification_needed`, answered through the draft routes), `ephemeral` and `expiresAt` on watch reads, and the emailed-manage-link operation `getManagedWatch` (`GET /api/manage/{token}`, now 404). Request and response summaries match the live API text.

## 0.3.1 (2026-11-27)

- Package metadata only (no API or behaviour change): author Velvee, Inc. <support@velvee.ai>, homepage https://www.percia.ai, repository, bugs, license MIT.

## 0.3.0 (2026-11-27)

- `events.stream(watch_id=, concern_id=, type=, backlog=, since=, max_reconnects=, idle_timeout=)`: iterator (sync) and async iterator (`AsyncPercia`) over the developer event feed (`GET /api/events/stream`, SSE). Yields `Open`, `Event` (`cursor`, parsed `event`, the exact `data` string), `Resync`, `End`, `Reconnect`, `Ping`. Reconnects with `Last-Event-ID`, backoff with jitter, `Retry-After` on 429, a read-timeout idle detector, dedupe on `eventId`; raises typed errors for 401/403/404/400 (no retry). `verify_webhook_signature` is unchanged.

- Billing (additive): `account.plan()`, `account.usage()` and `account.billing()` (a `Billing` dataclass shaped like the `billing` block of MCP `whoami`: `plan_label`, `free_minutes_remaining`, `credit_minutes`, `can_start_watches`, `how_charged`, `next_step`, ...); `billing_of(plan)` and `describe_billing(billing)`. Missing fields are `None`, never guessed.
- `cameras.create(name, device_kind=)`; `Camera.device_kind`. Sync and async.
- Regenerated from the current Percia API spec (146 operations).

## 0.2.0 (unreleased)

- Camera push (cameras on a private network): `cameras.register_push(name, external_id)` (idempotent; returns a `PushRegistration` with `whip_url` and the one-time `token`, or `existing=True, token=None`; `on_existing="return" | "rotate" | "throw"`), `cameras.rotate_token`, `cameras.revoke_token`, `cameras.status`, `cameras.bulk`; sync and async.
- Helpers that never carry the token: `build_publish_commands`, `publish_argv` (for spawning), `scrub_token`; `repr` of a registration hides the token.
- `cameras.status(id)` calls `GET /cameras/{id}/status` and returns a `CameraStatus` (`state`: `waiting | online | offline | revoked`, `status`, `last_seen_at`, `seconds_since_seen`, `watch_count`, `hint`). On a 404 (older server) it reads `GET /cameras` and derives the state (`derived=True`).
- `cameras.bulk(items, on_existing=)` calls `POST /cameras/bulk`, 10 per request (longer lists are chunked), results per item in input order; a 404 falls back to one `register_push` per item.
- Regenerated from the live spec (105 operations).

## 0.1.0 (unreleased)

- First version. Generated models and operations from the pinned OpenAPI document (95 operations), hand-written sync and async clients, retries with `Retry-After`, typed errors with `request_id`, event pagination iterators, `verify_webhook_signature` and `verify_and_parse`.
