# Changelog

## 0.3.3 (2026-11-27)

- `percia whoami` reads `GET /api/whoami`: account (masked for OAuth), key or app name and granted scopes; `--json` adds `identity`, and `account` is now filled for API keys too (`id`). A rejected credential exits 3. Hosts without the route fall back to the previous behaviour.

## 0.3.2 (2026-11-27)

- Synced with the Percia API after the Percia 2.0-only cleanup (145 operations). Removed from the generated models: `interpret`, `concerns`, `acknowledge`, `interpretation` and `runtime: "core"` on create and update watch (the API refuses them with 422 `invalid_request`; a goal is read by Percia's layer and an unclear one answers 422 `clarification_needed`, answered through the draft routes), `ephemeral` and `expiresAt` on watch reads, and the emailed-manage-link operation `getManagedWatch` (`GET /api/manage/{token}`, now 404). Request and response summaries match the live API text.

## 0.3.1 (2026-11-27)

- Package metadata only (no API or behaviour change): author Velvee, Inc. <support@velvee.ai>, homepage https://www.percia.ai, repository, bugs, license MIT.

## 0.3.0 (2026-11-27)

- `percia listen` follows `GET /api/events/stream` (SSE with fetch streaming) instead of polling `GET /api/events`: `--forward-to <url>` (alias `--forward`), `--watch`, `--concern`, `--type`, `--secret-env NAME`, `--secret-file PATH` (default `PERCIA_WEBHOOK_SECRET`; no `--secret <value>` any more), `--backlog N`, `--print` (JSON lines on stdout), `--replay <eventId>` (replaces `--replay <n>`), `--allow-remote`. Each event is POSTed with the exact data string, `content-type`, `Percia-Signature` and `x-percia-event-id` / `x-percia-delivery-id`, and a compact line is printed (type, short ids, local status, latency). Reconnects with `Last-Event-ID` and backoff, honours `Retry-After`, dedupes on `eventId`, backfills once after `resync`, explains 401/403/429/connection refused, never prints the key or the secret, exits 0 on Ctrl-C. `--interval` is gone.

- `percia plan` (alias `billing`): free minutes left this month and when they come back, credit minutes, minutes used, whether a new watch can start, how you are charged, the card bonus and the next step (`--json` adds a `billing` block to the raw plan). `percia whoami` shows the same block (and `billing` in `--json`; absent when the plan cannot be read).
- `cameras add --device-kind phone|tablet|computer`; `cameras list` has a device column.

## 0.2.0 (unreleased)

- `cameras push register --name --external-id [--rtsp]` prints the WHIP URL and the publish token once, with a warning; keeps a 0600 copy in the config directory (`--no-save` to skip).
- `cameras push run --rtsp URL`: registers (idempotently) and runs ffmpeg RTSP -> WHIP in the foreground with a heartbeat and restarts; checks for ffmpeg with the whip muxer and explains what is missing.
- `cameras token rotate|revoke <id>`, `cameras status [id]` (with an id it calls the status route and prints `state` and the server's hint; an older server without the route falls back to the camera list); `cameras list` shows kind and external id.

## 0.1.0 (unreleased)

- First release: `login` (browser OAuth 2.1 + PKCE, or an API key), `whoami`, `watches`, `events list --follow`, `cameras`, `destinations`, `hooks`, `listen`, `mcp setup`, `doctor`, `completion`.
