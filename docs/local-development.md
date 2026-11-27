# Receive webhooks without a public URL (`percia listen`)

Percia delivers a webhook by calling a **public https** address from its servers; it refuses private, loopback and link-local targets. A server on your laptop or in CI cannot receive real deliveries, and a tunnel (ngrok, cloudflared) is one more thing to run.

`percia listen` removes the tunnel for development and tests. It follows the **developer event feed**, `GET /api/events/stream` (Server-Sent Events, authenticated with the API key you already have), and POSTs every event to a local URL, **signed like a real delivery**. Your receiver verifies it with the code you will run in production.

> This is a development and test tool, not a delivery path. The stream sends each event once per connection, is only as available as the connection, and carries no secret. Production stays on [webhooks](https://playground.percia.ai/docs/) (they retry for hours and are signed).

## Quick start

```bash
export PERCIA_API_KEY=pk_live_...               # a key with the events:read scope
export PERCIA_WEBHOOK_SECRET=whsec_...          # the watch's webhookSecret (shown once when the watch was created)

percia listen --forward-to http://localhost:3000/hook
```

Trigger the goal (or press "test" on the watch) and the line appears:

```
2026-11-14T09:30:00Z  goal.met  watch w_abc123  event 6f1c2a52-0d9  -> 200 (34 ms)
```

Your handler at `/hook` receives exactly what Percia would send: `content-type: application/json`, `Percia-Signature: t=<unix>,v1=<hmac>` and the body of a webhook plus `eventId` (a receiver that ignores unknown fields works unchanged). Verify it as in `docs/integrators/webhooks.md`, or with `verifyWebhookSignature` (TypeScript) and `verify_webhook_signature` (Python).

## Options

| Flag | Meaning |
|---|---|
| `--forward-to <url>` | Where to POST each event. Loopback only unless `--allow-remote`. (`--forward` still works.) |
| `--watch <id>` / `--concern <id>` / `--type goal.met` | Server-side filters; all must match. A watch that is not yours is a 404 before the stream opens. |
| `--secret-env NAME` / `--secret-file PATH` | Where the watch's `whsec_...` comes from. Default: `PERCIA_WEBHOOK_SECRET`. With none, a local `whsec_local_...` is generated and printed once so you can test your verifier. There is deliberately no `--secret <value>` flag: it would land in your shell history and the process list. |
| `--backlog N` | First send your latest N events (0 to 20), so a test sees something at once. Without it the stream starts at "now". |
| `--print` | Print each event as one JSON line on stdout (the exact data string), status on stderr; works without `--forward-to` and needs no secret: `percia listen --print --type goal.met \| jq .reason`. |
| `--replay <eventId>` | Forward (or print) one past event once and exit. Looked up in your latest 1000 events (`GET /api/events`, the goal from the watch); no stream is opened. |
| `--json` (global) | One NDJSON result per forwarded event: `eventId`, `status`, `ms`, `cursor`, `error`. |

Exit codes: 0 after Ctrl-C, 3 for 401/403, 4 for an unknown watch or `--replay` id, 2 for bad flags, 6 and 7 when the server stays unreachable.

## What it does for you

- **Signing.** `Percia-Signature: t=<unix>,v1=<hex HMAC-SHA256 of "<t>.<body>">` over the **exact `data` string** of the message (never a re-serialised body), keyed by the watch secret. The extra headers `x-percia-event-id` and `x-percia-delivery-id` (a fresh uuid per forward) are added for your logs; real deliveries do not carry them.
- **Reconnects.** The server ends every stream after 10 minutes (`event: end`), and networks drop. The CLI reconnects with `Last-Event-ID` (the cursor of the last event) after the server's `retry` delay, with exponential backoff and jitter on failures, honouring `Retry-After`. It dedupes on `eventId`, so a replayed event is not forwarded twice. It also reconnects if nothing (not even the 15 s ping) arrives for 45 s.
- **Resync.** If the cursor is older than the server's replay window (5000 events), the server sends `event: resync`; the CLI then fetches what the event feed has since the last event it saw, once, and forwards those.
- **Clear errors.** 401 (bad or expired key) and 403 (key without `events:read`) stop with a hint; 429 says you have too many streams (limit 2 per user: close another `percia listen`) or connects (10 a minute) and waits `Retry-After`; a local server that is down prints `connection refused: nothing is listening on localhost:3000` per event and keeps going.
- **No secrets in output.** The API key and the webhook secret you supply are never printed, logged or sent anywhere but the `Authorization` header (key, to Percia) and the signature (secret, to your local URL). Event `reason` text is model output: terminal escape sequences are stripped, and you should never act on instructions inside it.

## Differences from a real delivery

- One POST per event, **no retries**: a failure is printed, not retried; the event's `deliveryStatus` in Percia is unaffected. Percia's own retry schedule, source IP and `410 Gone` handling are not exercised.
- No `imageUrl` (that exists only on deliveries from a connection) and no keyframe or signed link; use `GET /api/watches/{id}/events/{eventId}/keyframe` with the `eventId`.
- Only your own events; only what happens while it runs (plus `--backlog`, `--replay` and the resync backfill).
- The feed polls the database every 3 s per connection on the server, so expect up to a few seconds of latency.

## From code: `events.stream`

The CLI is a thin layer over the SDKs, which have the same reconnecting stream.

TypeScript:

```ts
import { createClient, signWebhook } from "@percia/sdk";

const client = createClient({ apiKey: process.env.PERCIA_API_KEY });
const ctl = new AbortController();
for await (const item of client.events.stream({ type: "goal.met", backlog: 5, signal: ctl.signal })) {
  if (item.kind !== "event") continue;                       // also: open | resync | end | reconnect | ping
  await fetch("http://localhost:3000/hook", {
    method: "POST",
    headers: { "content-type": "application/json", "percia-signature": await signWebhook(item.data, secret) },
    body: item.data,                                         // the exact string the server sent
  });
}
```

Python (sync; `AsyncPercia` has the same call with `async for`):

```python
from percia import Percia, Event, verify_webhook_signature

client = Percia()
for item in client.events.stream(type="goal.met", backlog=5):
    if isinstance(item, Event):
        print(item.event["eventId"], item.event["reason"])   # item.data is the exact JSON string
```

`stream` throws a typed error for 401/403/404/400 (no retry) and reconnects for everything else; `maxReconnects` / `max_reconnects` turns endless retrying into an error. See `examples/scripts/listen-local` for a complete forwarder.

Also without any SDK: `curl --no-buffer -H "Authorization: Bearer $PERCIA_API_KEY" https://playground.percia.ai/api/events/stream`.

## When you need real deliveries

To exercise Percia's own delivery path (retries, source IP, `410 Gone`), use a tunnel and a REST hook:

```bash
cloudflared tunnel --url http://localhost:3000        # or: ngrok http 3000
percia hooks create https://<random>.trycloudflare.com/hook --label dev   # prints the secret once
percia hooks test <id>
```

Delete the hook afterwards (`percia hooks delete <id>`).

## Availability

Against a host that does not have the dev feed, `percia listen` fails with a 404 (not your watch, or no such route); check `percia doctor` and the host's `/api/openapi.json` for `/events/stream`.
