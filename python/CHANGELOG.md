# Changelog

## 0.2.0 (unreleased)

- Camera push (cameras on a private network): `cameras.register_push(name, external_id)` (idempotent; returns a `PushRegistration` with `whip_url` and the one-time `token`, or `existing=True, token=None`; `on_existing="return" | "rotate" | "throw"`), `cameras.rotate_token`, `cameras.revoke_token`, `cameras.status`, `cameras.bulk`; sync and async.
- Helpers that never carry the token: `build_publish_commands`, `publish_argv` (for spawning), `scrub_token`; `repr` of a registration hides the token.
- Regenerated from a spec that adds `POST/DELETE /cameras/{id}/token` and `kind`, `external_id` on cameras.

## 0.1.0 (unreleased)

- First version. Generated models and operations from the pinned OpenAPI document (95 operations), hand-written sync and async clients, retries with `Retry-After`, typed errors with `request_id`, event pagination iterators, `verify_webhook_signature` and `verify_and_parse`.
