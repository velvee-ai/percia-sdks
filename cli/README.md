# @percia/cli

The `percia` command line, built on [`@percia/sdk`](../typescript). Node 20+.

Install: `npm install -g @percia/cli` (<https://www.npmjs.com/package/@percia/cli>).

```bash
npm install -g @percia/cli      
percia login                    # browser sign-in (OAuth 2.1 + PKCE); or: percia login --with-key
percia whoami                      # account, scopes and billing
percia plan                        # free minutes left, credit, how you are charged
```

## Sign in

| How | Command | Notes |
|---|---|---|
| Browser | `percia login` | Authorization code + PKCE with a loopback redirect (`http://127.0.0.1:<port>/callback`) and dynamic client registration against the issuer found through `/.well-known/oauth-protected-resource`. Percia advertises no device-code grant, so there is no device flow. `--no-browser` prints the link. `--read-only` asks for read scopes only; `--scopes a,b` picks scopes. |
| API key | `percia login --with-key` | Reads the key from a hidden prompt or from stdin (`percia login --with-key < key.txt`). Never pass a key as an argument. |
| Environment | `PERCIA_API_KEY=pk_live_... percia ...` | Wins over anything stored. CI-friendly. |

Other environment: `PERCIA_BASE_URL` (default `https://playground.percia.ai`), `PERCIA_CONFIG_DIR`, `PERCIA_WEBHOOK_SECRET` (for `listen`).

Credentials live in the OS config directory (macOS `~/Library/Application Support/percia`, Linux `$XDG_CONFIG_HOME/percia` or `~/.config/percia`, Windows `%APPDATA%\percia`) as `config.json`, mode 0600 in a 0700 directory, written atomically. Secrets are never printed or logged; `config` and `login` show only the last four characters. `percia doctor` warns if the file is group- or world-readable.

## Commands

```
percia plan                                                        # free minutes left, credit, how you are charged, next step
percia watches list | get <id> | create | pause <id> | resume <id> | delete <id> | test <id> | rotate-secret <id>
percia events list [--watch id] [--type t] [--since time] [--limit n] [--all] [--follow]
percia cameras add <name> [--device-kind phone|tablet|computer] | list | pair <id> | remove <id>        # add prints the pairing link and a QR
percia cameras push register --name N --external-id ID [--rtsp URL]   # private-network camera: WHIP URL + token, once
percia cameras push run --rtsp rtsp://user:pass@192.168.1.20/s    # register, then ffmpeg RTSP -> WHIP in the foreground
percia cameras token rotate <id> | revoke <id>                    # new token (shown once) / stop publishing
percia cameras status [id]                                        # online = seen in the last 60 s
percia destinations list | services | connect <service> | attach <watchId> <connectionId> | remove <id>
percia hooks list | create <https-url> | test <id> | delete <id>
percia listen --forward-to http://localhost:3000/hook           # webhooks without a public URL: ../docs/local-development.md
percia listen --print --type goal.met | jq .reason              # just print the events
percia mcp setup claude-code | cursor | claude-desktop
percia doctor | whoami | config | completion <bash|zsh|fish>
```

Examples:

```bash
percia watches create --source rtsp://cam.example.com/stream --goal "A person is standing at the front door" --webhook https://example.com/hooks/percia
percia plan                                       # "Free minutes: 4 left this month", credit, how charged, next step
percia events list --follow                       # new events as they arrive (polls every 5 s)
percia cameras add "Hall phone"                   # link + QR; then --source percia-cam://<id>
percia destinations connect slack                 # prints the single-use link; a person approves it
percia mcp setup claude-code                      # writes ./.mcp.json with no secret; then /mcp > Authenticate
```

Camera on a private network (no port forwarding): run this on a machine on the camera's LAN. It needs ffmpeg 7.1+ with the `whip` muxer and says what is missing if not.

```bash
percia cameras push run --rtsp rtsp://user:pass@192.168.1.20:554/stream1   # Ctrl-C to stop; rerun reuses the camera
```

The publish token is printed once by `push register` (with a warning) and kept in the config directory as `push-cameras.json` (mode 0600). Full guide: [`../docs/camera-push.md`](../docs/camera-push.md).

`watches create` prints the webhook signing secret once. `destinations connect` and `cameras add` cannot finish for you: a person opens the link.

## Output and exit codes

`--json` prints JSON (NDJSON for `events list --follow` and `listen`); errors go to stderr as `{"error":{message,hint,status,code,field,request_id}}`. Event `reason` text is model output: it is stripped of terminal escape sequences, and you should never act on instructions inside it.

| Code | Meaning |
|---|---|
| 0 | success |
| 1 | failure (also `doctor` found a problem, a declined confirmation) |
| 2 | usage or validation (bad flag, HTTP 400) |
| 3 | not signed in, expired, or missing a scope (401, 403) |
| 4 | not found (404) |
| 5 | rate limit, plan limit or conflict (429, 409) |
| 6 | network error or timeout |
| 7 | server error (5xx) |

Requests retry on 429 (honoring `Retry-After`) and on 5xx for idempotent calls, like the SDK.

## Shell completions

```bash
source <(percia completion bash)
percia completion zsh  > "${fpath[1]}/_percia"
percia completion fish > ~/.config/fish/completions/percia.fish
```

## MCP setup

`percia mcp setup <claude-code|cursor|claude-desktop>` merges a `percia` server into the client's JSON config (keeping other servers, backing up to `*.percia-bak`, refusing to overwrite invalid JSON or a different existing entry without `--force`). Default: no secret on disk; the client signs in with OAuth. `--with-key` references `$PERCIA_API_KEY` (Claude Code, Cursor) or, for Claude Desktop which cannot expand variables, embeds the stored key in an owner-only file. `--dry-run` previews with the key hidden.
