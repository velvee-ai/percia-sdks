# Changelog

Per-package changelogs: [typescript](typescript/CHANGELOG.md), [cli](cli/CHANGELOG.md), [python](python/CHANGELOG.md).

## 0.3.2 (2026-11-27)

- Synced with the Percia API after the Percia 2.0-only cleanup (145 operations). Removed from the generated models: `interpret`, `concerns`, `acknowledge`, `interpretation` and `runtime: "core"` on create and update watch (the API refuses them with 422 `invalid_request`; a goal is read by Percia's layer and an unclear one answers 422 `clarification_needed`, answered through the draft routes), `ephemeral` and `expiresAt` on watch reads, and the emailed-manage-link operation `getManagedWatch` (`GET /api/manage/{token}`, now 404). Request and response summaries match the live API text.
- CI: the Python matrix runs on `ubuntu-24.04` (Python 3.9 is not on `ubuntu-latest` any more), and the npm release workflow publishes only when the repository variable `NPM_TRUSTED_PUBLISHING` is `true` (it is not set up yet, releases are published by hand).

## 0.3.1 (2026-11-27)

- Metadata release of `@percia/sdk`, `@percia/cli` and `percia` (author, homepage https://www.percia.ai, bugs, repository, license); no code change.

## 0.3.0 (2026-11-27)

- First public release on npm (`@percia/sdk`, `@percia/cli`) and PyPI (`percia`).

- Synced with the current Percia API (146 operations). `GET /api/plan` (and MCP `whoami`) carry the billing block (`label`, `freeMinutesLeft`, `creditMinutes`, `canStartWatches`, `howCharged`, `nextStep`, ...); cameras carry `deviceKind` (`phone | tablet | computer | null`). TypeScript: `account.billing()`, `billingOf`, `describeBilling`, `cameras.create(name, { deviceKind })`. Python: `account.plan/usage/billing`, `billing_of`, `describe_billing`, `cameras.create(name, device_kind=)`. CLI: `percia plan`, a billing block in `whoami`, `cameras add --device-kind`.
- `percia listen`, the local-development webhook forwarder, runs on the developer event feed `GET /api/events/stream` (SSE): events arrive live, are POSTed to a local URL signed exactly like real webhooks, and the CLI reconnects with `Last-Event-ID`, backs off, honours `Retry-After` and dedupes on `eventId`. SDK: `events.stream()` in TypeScript and Python (sync and async).
- Camera push for cameras on a private network: SDK methods in both languages (`registerPush`, `rotateToken`, `revokeToken`, `status`, `bulk`), publish-command helpers, `percia cameras push|token|status`, Postman entries and `examples/scripts/push-lan-camera`.
- Initial release of the monorepo: pinned OpenAPI document, TypeScript SDK, Python SDK, CLI, Postman/Insomnia, examples, CI and release workflows.
