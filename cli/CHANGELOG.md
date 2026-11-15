# Changelog

## 0.2.0 (unreleased)

- `cameras push register --name --external-id [--rtsp]` prints the WHIP URL and the publish token once, with a warning; keeps a 0600 copy in the config directory (`--no-save` to skip).
- `cameras push run --rtsp URL`: registers (idempotently) and runs ffmpeg RTSP -> WHIP in the foreground with a heartbeat and restarts; checks for ffmpeg with the whip muxer and explains what is missing.
- `cameras token rotate|revoke <id>`, `cameras status [id]` (with an id it calls the status route and prints `state` and the server's hint; an older server without the route falls back to the camera list); `cameras list` shows kind and external id.

## 0.1.0 (unreleased)

- First release: `login` (browser OAuth 2.1 + PKCE, or an API key), `whoami`, `watches`, `events list --follow`, `cameras`, `destinations`, `hooks`, `listen`, `mcp setup`, `doctor`, `completion`.
