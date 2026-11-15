# Changelog

Per-package changelogs: [typescript](typescript/CHANGELOG.md), [cli](cli/CHANGELOG.md), [python](python/CHANGELOG.md).

## Unreleased

- Camera push for cameras on a private network: SDK methods in both languages (`registerPush`, `rotateToken`, `revokeToken`, `status`, `bulk`), publish-command helpers, `percia cameras push|token|status`, Postman entries, `examples/scripts/push-lan-camera` (Node and Python). Versions bumped to 0.2.0 (nothing published). The spec pin is the live document again (105 operations; percia-cf master `bb95c92` is deployed), so it includes `POST /cameras/bulk`, `GET /cameras/{id}/status`, the token routes, the `/cam/claim` body and the newer billing/credits routes. `cameras.status` and `cameras.bulk` use the real routes in both SDKs (a 404 means an older server: they fall back to `GET /cameras` and to per-item registration). Spec drift check is green.

- Monorepo created: pinned OpenAPI document, TypeScript SDK, Python SDK, CLI, Postman/Insomnia, examples, CI and release workflows.
