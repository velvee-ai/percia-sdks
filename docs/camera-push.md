# Cameras on a private network (camera push)

Almost every home or office RTSP camera sits on a private LAN. Percia never pulls from private hosts, and port-forwarding is not a good answer. A small connector on the LAN pulls the camera **once** and pushes it to Percia over WHIP (WebRTC). The camera serves a single RTSP session however many things use the stream.

Server contract: `percia-cf/docs/specs/cameras/camera-push-api.md` and ADR 0042. Recorded for the tests in [`spec/camera-push-contract.json`](../spec/camera-push-contract.json). **The server side was not yet deployed when this was written** (see [assumptions](#assumptions-to-re-check)).

## The flow

1. `POST /api/cameras {name, kind:"push", externalId}` -> `201 {camera, whipUrl, token, expiresAt:null, publish}`. `token` (`pc_...`) is a bearer secret for publishing to that one camera. It is shown **once**.
2. Publish WHIP to `whipUrl` with `Authorization: Bearer <token>` (ffmpeg, OBS, GStreamer, or Percia Bridge). While publishing, `POST /api/cam/heartbeat` (Bearer token) every 20 s. Online means seen in the last 60 s.
3. Register again with the same `externalId`: `200 {camera, whipUrl, token:null, existing:true}`. Nothing is created and **no token comes back**. Keep the first one, or rotate.
4. `POST /api/cameras/:id/token` rotates (the old token dies at once); `DELETE /api/cameras/:id/token` revokes (publishing stops, the camera stays). Both need `cameras:write` and `watches:delete`. A phone camera answers `409 wrong_kind`.
5. Create a watch on it as usual: `--source percia-cam://<cameraId>`.

## Fastest path: the CLI

```bash
export PERCIA_API_KEY=pk_live_...        # scope cameras:write (rotate also needs watches:delete)
percia cameras push run --rtsp rtsp://user:pass@192.168.1.20:554/stream1
# registers (idempotently), then runs ffmpeg RTSP -> WHIP in the foreground with a heartbeat; Ctrl-C stops it
percia watches create --source percia-cam://<cameraId> --goal "A person is at the door"
```

- Needs **ffmpeg 7.1 or newer built with the `whip` muxer** (`ffmpeg -muxers | grep whip`). The command checks first and says what is missing: macOS `brew install ffmpeg`, Debian/Ubuntu `apt install ffmpeg` (check the version), or a recent static build. If you cannot get it, `percia cameras push register --rtsp ...` prints OBS and GStreamer settings.
- `--mode transcode` re-encodes to 720p / 10 fps / H.264 baseline for H.265 or heavy streams (`copy` is the default and needs H.264).
- The camera id defaults to a hash of the RTSP address, so running it again reuses the same Percia camera. Set `--external-id` to choose your own.
- The token is saved in `<config dir>/push-cameras.json` (mode 0600, directory 0700; `~/.config/percia` on Linux, `~/Library/Application Support/percia` on macOS). A rerun reuses it. If the camera exists but this machine has no saved token, the command stops and tells you to pass `--rotate`. `--no-save` on `register` keeps nothing on disk.
- Other commands: `percia cameras push register --name N --external-id ID [--rtsp URL]` (prints URL and token once, with a warning), `percia cameras token rotate|revoke <id>`, `percia cameras status [id]`.

**Where the secrets are visible.** ffmpeg takes the token (`-authorization`) and the RTSP credentials as command-line arguments, so other users on the same machine can see them in `ps`. Run the connector on a machine you control. The CLI never prints the token except once at registration, scrubs it from ffmpeg's output, and prints the RTSP address without its password.

## SDKs

```ts
import { createClient, buildPublishCommands } from "@percia/sdk";
const percia = createClient({ apiKey: process.env.PERCIA_API_KEY });

const reg = await percia.cameras.registerPush({ name: "Front door", externalId: "front-door" });
if (reg.token) saveSecurely(reg.token);          // first call only: shown once
// reg.existing === true && reg.token === null: a later call. Use onExisting: "rotate" to mint a new one, or "throw".
const cmds = buildPublishCommands(reg, { rtsp: "rtsp://user:pass@192.168.1.20/stream1" });
console.log(cmds.ffmpeg);                         // uses "$PERCIA_CAMERA_TOKEN", never the token
```

```python
from percia import Percia, build_publish_commands

percia = Percia(api_key=os.environ["PERCIA_API_KEY"])
reg = percia.cameras.register_push("Front door", "front-door")   # on_existing="return" | "rotate" | "throw"
if reg.token:
    save_securely(reg.token)                       # first call only: shown once
print(build_publish_commands(reg.whip_url, "rtsp://user:pass@192.168.1.20/stream1")["ffmpeg"])
```

| | TypeScript | Python |
|---|---|---|
| register (idempotent) | `cameras.registerPush({name, externalId, onExisting?})` | `cameras.register_push(name, external_id, on_existing=)` |
| new token (once) | `cameras.rotateToken(id)` | `cameras.rotate_token(id)` |
| stop publishing | `cameras.revokeToken(id)` | `cameras.revoke_token(id)` |
| one camera's state | `cameras.status(id)` | `cameras.status(id)` |
| many cameras | `cameras.bulk([{name, externalId}], {concurrency})` | `cameras.bulk([{"name", "external_id"}])` |
| list / delete | `cameras.list()` / `cameras.delete(id)` | same |
| publish commands | `buildPublishCommands`, `publishArgv` (argv, for spawning), `scrubToken`, `redactRegistration` | `build_publish_commands`, `publish_argv`, `scrub_token` |

Errors are the usual typed ones with `.code`: `camera_limit` (429, 10 per user), `wrong_kind` (409), validation on `externalId` (400, `field`), `insufficient_scope` (403). `status` and `bulk` are built on `GET /cameras` and `registerPush` because the API has no per-camera status route and no bulk route; `bulk` reports each item (`ok`, `registration` or `error`) and one failure does not stop the others.

**Never logging the token.** Printable commands use the literal `$PERCIA_CAMERA_TOKEN` (export it, or let your connector read it from a file). `redactRegistration(reg)` and Python's `repr(reg)` hide it. `publishArgv` / `publish_argv` do take the real token, because spawning a process needs it: pass them to `spawn`, not to a logger.

## Templates

[`examples/scripts/push-lan-camera/`](../examples/scripts/push-lan-camera): `push.mjs` (Node) and `push.py` (Python), "push an RTSP camera from my LAN": register, keep the token in a 0600 file, run ffmpeg, heartbeat, restart on failure. Postman: folder "Cameras (phone and push)" has the push create request and rotate/revoke; it saves `cameraId`, `whipUrl` and `cameraToken`.

## Assumptions to re-check

- Request and response shapes above come from the spec and the draft OpenAPI on the unmerged percia-cf branch. The pinned `spec/openapi.json` merges only `/cameras`, `/cameras/{id}/token` and `Camera` from that draft into the live pin; everything else is the live document. Re-sync once the server is deployed (`pnpm spec:sync && pnpm generate`).
- `GET /cameras/:id/status` and a bulk route were mentioned in the brief but are not in the spec (bulk create is listed as a non-goal). If they appear, switch `status` and `bulk` to them.
- `ffmpeg -f whip -authorization <token>` is the documented publish path (the server's `publish.ffmpegCopy` example uses it). The GStreamer line (`whipclientsink`, `signaller::auth-token`) and the OBS note follow the upstream docs and are **not** verified against a live Percia host.
- Heartbeat: `POST /api/cam/heartbeat` with the camera token, every 20 s; a successful publish also marks the camera seen.
- A watch whose camera sends no video for 60 minutes is paused (`pausedReason` `no_video`) and the owner is emailed, as for phone cameras (server doc, not an SDK concern). Reconnect WHIP with backoff 1 s doubling to 30 s and keep the same token (the CLI and the templates restart ffmpeg this way).
- 402 `payment_required` and 404 (phone cameras switched off) pass through as typed errors.
