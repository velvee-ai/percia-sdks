# `percia listen`: forwarding events to localhost

Percia delivers a webhook by calling a **public https** address from its servers; it refuses private, loopback and link-local targets (see limits). So a server on your laptop cannot receive real deliveries, and there is no relay in Percia today (nothing like `stripe listen`, which holds a connection open from the server to your machine).

## What `listen` does

`percia listen --forward http://localhost:3000/hook` polls `GET /api/events` (scope `events:read`), takes events newer than what it has seen (dedupe on the event `id`, as the REST-hook docs describe for polling triggers), and POSTs each one to your local URL with:

- the documented body: `{id, watchId, occurrenceId, type, goal, reason, confidence, at}` (`id` is the decision id, `goal` is looked up from the watch),
- `content-type: application/json` and a `Percia-Signature: t=<unix>,v1=<hmac>` header computed exactly like a real delivery.

Signing key: `--secret whsec_...` (or `PERCIA_WEBHOOK_SECRET`). Use the watch's or hook's real secret and your receiver verifies **unchanged**, as in production. Without one the CLI generates `whsec_local_...` and prints it once.

## Differences from a real delivery (the limitation)

- It is emulation by polling: latency is the poll interval (default 3 s, minimum 2 s), not instant.
- No retries: one POST per event; a failure is printed, not retried. The event's `deliveryStatus` in Percia is unaffected.
- No `imageUrl` (that field exists only on connection deliveries), and no `goal.test` events.
- Percia's own delivery is not exercised: its source IP, retry schedule and `410 Gone` handling are not tested.
- Events that happened while `listen` was not running are skipped unless `--replay <n>`.
- `--forward` must be loopback unless `--allow-remote`: event text is sent there.

## Real deliveries to your machine today

Use a tunnel and a REST hook, which is the production path:

```bash
cloudflared tunnel --url http://localhost:3000        # or: ngrok http 3000
percia hooks create https://<random>.trycloudflare.com/hook --label dev   # prints the secret once
percia hooks test <id>
```

Delete the hook afterwards (`percia hooks delete <id>`).

## What a true relay needs (server change, not done)

Either (a) an authenticated stream endpoint (SSE or WebSocket, e.g. `GET /api/events/stream`) that pushes events as they are recorded, which `listen` would use instead of polling, or (b) a relay hook type: `POST /api/hooks {url: "percia-relay://<session>"}` where deliveries are queued for a connected CLI. Neither exists on percia-cf master; this was not invented here.
