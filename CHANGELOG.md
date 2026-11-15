# Changelog

Per-package changelogs: [typescript](typescript/CHANGELOG.md), [cli](cli/CHANGELOG.md), [python](python/CHANGELOG.md).

## Unreleased

- Camera push for cameras on a private network: SDK methods in both languages (`registerPush`, `rotateToken`, `revokeToken`, `status`, `bulk`), publish-command helpers, `percia cameras push|token|status`, Postman entries, `examples/scripts/push-lan-camera` (Node and Python). Versions bumped to 0.2.0 (nothing published). The spec pin now carries the push routes from percia-cf branch `divi-vijayakumar/camera-push-api` (not yet deployed): re-sync once it is live.

- Monorepo created: pinned OpenAPI document, TypeScript SDK, Python SDK, CLI, Postman/Insomnia, examples, CI and release workflows.
