# Changelog

Per-package changelogs: [typescript](typescript/CHANGELOG.md), [cli](cli/CHANGELOG.md), [python](python/CHANGELOG.md).

## Unreleased

- `percia listen`, the local-development webhook forwarder, now runs on the developer event feed `GET /api/events/stream` (SSE) instead of polling: events arrive live, are POSTed to a local URL signed exactly like real webhooks (`Percia-Signature` over the exact data string), and the CLI reconnects with `Last-Event-ID`, backs off, honours `Retry-After`, dedupes on `eventId` and backfills after `resync`. `--forward-to`, `--watch`, `--concern`, `--type`, `--secret-env`, `--secret-file`, `--backlog`, `--print`, `--replay <eventId>`. SDK: `events.stream()` (TypeScript async iterator, Python sync iterator and async iterator) with the same reconnect logic, `parseSse`. Docs: `docs/local-development.md`; example `examples/scripts/listen-local`; mock-server tests for framing, resume, signing and backoff. Versions bumped to 0.3.0 (nothing published). Breaking inside the unreleased 0.2.0 line: `listen --secret <value>` is gone (use `--secret-env`/`--secret-file`), `--forward` is an alias of `--forward-to`, `--replay <n>` and `--interval` are replaced.

- Camera push for cameras on a private network: SDK methods in both languages (`registerPush`, `rotateToken`, `revokeToken`, `status`, `bulk`), publish-command helpers, `percia cameras push|token|status`, Postman entries, `examples/scripts/push-lan-camera` (Node and Python). Versions bumped to 0.2.0 (nothing published). The spec pin is the live document again (105 operations; percia-cf master `bb95c92` is deployed), so it includes `POST /cameras/bulk`, `GET /cameras/{id}/status`, the token routes, the `/cam/claim` body and the newer billing/credits routes. `cameras.status` and `cameras.bulk` use the real routes in both SDKs (a 404 means an older server: they fall back to `GET /cameras` and to per-item registration). Spec drift check is green.

- Monorepo created: pinned OpenAPI document, TypeScript SDK, Python SDK, CLI, Postman/Insomnia, examples, CI and release workflows.
