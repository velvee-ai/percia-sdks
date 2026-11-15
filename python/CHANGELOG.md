# Changelog

## 0.2.0 (unreleased)

- Camera push (cameras on a private network): `cameras.register_push(name, external_id)` (idempotent; returns a `PushRegistration` with `whip_url` and the one-time `token`, or `existing=True, token=None`; `on_existing="return" | "rotate" | "throw"`), `cameras.rotate_token`, `cameras.revoke_token`, `cameras.status`, `cameras.bulk`; sync and async.
- Helpers that never carry the token: `build_publish_commands`, `publish_argv` (for spawning), `scrub_token`; `repr` of a registration hides the token.
- `cameras.status(id)` calls `GET /cameras/{id}/status` and returns a `CameraStatus` (`state`: `waiting | online | offline | revoked`, `status`, `last_seen_at`, `seconds_since_seen`, `watch_count`, `hint`). On a 404 (older server) it reads `GET /cameras` and derives the state (`derived=True`).
- `cameras.bulk(items, on_existing=)` calls `POST /cameras/bulk`, 10 per request (longer lists are chunked), results per item in input order; a 404 falls back to one `register_push` per item.
- Regenerated from the live spec (105 operations).

## 0.1.0 (unreleased)

- First version. Generated models and operations from the pinned OpenAPI document (95 operations), hand-written sync and async clients, retries with `Retry-After`, typed errors with `request_id`, event pagination iterators, `verify_webhook_signature` and `verify_and_parse`.
