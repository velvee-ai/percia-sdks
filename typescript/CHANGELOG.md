# Changelog

## 0.2.0 (unreleased)

- Camera push (cameras on a private network): `cameras.registerPush({ name, externalId })` (idempotent; returns `whipUrl` and the one-time `token`, or `existing: true, token: null`; `onExisting: "return" | "rotate" | "throw"`), `cameras.rotateToken`, `cameras.revokeToken`, `cameras.status`, `cameras.bulk`.
- Helpers that never carry the token: `buildPublishCommands` (ffmpeg, OBS, GStreamer, heartbeat), `publishArgv` (for spawning), `redactRegistration`, `scrubToken`.
- Regenerated from a spec that adds `POST/DELETE /cameras/{id}/token` and `kind`, `externalId` on cameras.

## 0.1.0 (unreleased)

- First release. Typed client generated from the Percia OpenAPI document with `@hey-api/openapi-ts`; hand-written layer for auth, retries, typed errors, cursor pagination and webhook signature verification.
