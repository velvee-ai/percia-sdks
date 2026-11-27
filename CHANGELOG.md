# Changelog

Per-package changelogs: [typescript](typescript/CHANGELOG.md), [cli](cli/CHANGELOG.md), [python](python/CHANGELOG.md).

## 0.3.1 (2026-11-27)

- Metadata release of `@percia/sdk`, `@percia/cli` and `percia` (author, homepage https://www.percia.ai, bugs, repository, license); no code change.

## 0.3.0 (2026-11-27)

- First public release on npm (`@percia/sdk`, `@percia/cli`) and PyPI (`percia`).

- Synced with the current Percia API (146 operations). `GET /api/plan` (and MCP `whoami`) carry the billing block (`label`, `freeMinutesLeft`, `creditMinutes`, `canStartWatches`, `howCharged`, `nextStep`, ...); cameras carry `deviceKind` (`phone | tablet | computer | null`). TypeScript: `account.billing()`, `billingOf`, `describeBilling`, `cameras.create(name, { deviceKind })`. Python: `account.plan/usage/billing`, `billing_of`, `describe_billing`, `cameras.create(name, device_kind=)`. CLI: `percia plan`, a billing block in `whoami`, `cameras add --device-kind`.
- `percia listen`, the local-development webhook forwarder, runs on the developer event feed `GET /api/events/stream` (SSE): events arrive live, are POSTed to a local URL signed exactly like real webhooks, and the CLI reconnects with `Last-Event-ID`, backs off, honours `Retry-After` and dedupes on `eventId`. SDK: `events.stream()` in TypeScript and Python (sync and async).
- Camera push for cameras on a private network: SDK methods in both languages (`registerPush`, `rotateToken`, `revokeToken`, `status`, `bulk`), publish-command helpers, `percia cameras push|token|status`, Postman entries and `examples/scripts/push-lan-camera`.
- Initial release of the monorepo: pinned OpenAPI document, TypeScript SDK, Python SDK, CLI, Postman/Insomnia, examples, CI and release workflows.
