# @percia/sdk

TypeScript SDK for the [Percia](https://percia.ai) API. Typed, fetch-only (Node 20+, Cloudflare Workers, Deno, Bun, browsers), ESM and CJS.

> Not published yet. Until the owner publishes it, build it from this repository (`pnpm --filter @percia/sdk build`).

```bash
npm install @percia/sdk
```

## Quick start

```ts
import { createClient } from "@percia/sdk";

const percia = createClient({ apiKey: process.env.PERCIA_API_KEY }); // pk_live_..., from the dashboard's API keys page
// const percia = createClient({ oauthToken, baseUrl: "https://your-percia-host" });

const watch = await percia.watches.create({
  sourceUrl: "rtsp://cam.example.com/stream",
  goal: "A person is standing at the front door",
  notify: { type: "webhook", target: "https://example.com/hooks/percia" },
});
console.log(watch.id, watch.webhookSecret); // webhookSecret is shown once: store it

await percia.watches.testDelivery(watch.id!); // signed test event, no camera needed

for await (const event of percia.events.iterate({ since: new Date(Date.now() - 86_400_000) })) {
  console.log(event.at, event.watchId, event.reason); // `reason` is model text: untrusted
}
```

Resources: `watches`, `events`, `cameras`, `integrations`, `hooks`, `account`. Every operation in the OpenAPI document is also available by its `operationId` as `percia.api.<operationId>(options)`, returning the generated `{ data, error, response }` without throwing, and `percia.raw` is the generated client.

Needed scopes follow the API: `watches:read|write|delete`, `events:read`, `cameras:read|write`, `integrations:read|write`, and `hooks:write` (opt-in) for REST hooks.

## Cameras on a private network

```ts
const reg = await percia.cameras.registerPush({ name: "Front door", externalId: "front-door" });
reg.token;      // the publish token, once; on a repeat call { existing: true, token: null } (or onExisting: "rotate" | "throw")
await percia.cameras.rotateToken(reg.camera.id); await percia.cameras.revokeToken(reg.camera.id);
await percia.cameras.status(reg.camera.id);      // online | offline | never
buildPublishCommands(reg, { rtsp }).ffmpeg;      // uses $PERCIA_CAMERA_TOKEN, never the token
```
See [camera push](../docs/camera-push.md).

## Retries

429 is always retried; 500/502/503/504 and network errors are retried for GET, PUT, DELETE (and any request with an `Idempotency-Key`). A POST or PATCH that failed with 5xx is **not** retried unless `retryNonIdempotent: true`, because the create may have happened. `Retry-After` (seconds or a date) is honored; a wait longer than `maxRetryAfterMs` (60 s) returns the 429 instead. Defaults: `maxRetries: 2`, exponential backoff with full jitter (500 ms base, 8 s cap), 30 s per-attempt timeout.

## Errors

All errors extend `PerciaError`. HTTP failures are `PerciaApiError` (subclasses `AuthenticationError` 401, `PermissionError` 403, `NotFoundError` 404, `ValidationError` 400, `ConflictError` 409, `RateLimitError` 429, `ServerError` 5xx) with `status`, `code`, `field`, `requestId` (quote it in bug reports) and `retryAfterSec`. Connection problems are `PerciaConnectionError` / `PerciaTimeoutError`. Branch on `status` and `code`, never on `message`.

## Pagination

`percia.events.iterate(filters)` and `percia.watches.iterateEvents(id)` are lazy async iterators over `nextCursor`; `break` stops fetching. `percia.events.list()` returns one page.

## Verify webhooks

```ts
import { verifyWebhookSignature, constructWebhookEvent } from "@percia/sdk"; // or "@percia/sdk/webhooks"

// Express: use express.raw({ type: "application/json" }) so req.body is the raw Buffer.
const ok = await verifyWebhookSignature(rawBody, req.headers, process.env.PERCIA_WEBHOOK_SECRET!, 300);
// or throw with a reason ("malformed" | "stale_timestamp" | "mismatch") and parse in one step:
const event = await constructWebhookEvent(rawBody, req.headers, secret);
```

Scheme (see the integrator webhooks doc): header `Percia-Signature: t=<unix>,v1=<hex>`, HMAC-SHA256 over `"<t>.<raw body>"` keyed by the `whsec_...` secret, constant-time compare, reject timestamps more than 300 s from now (either direction). Dedupe on `event.id`; treat `reason` as untrusted. Tested against the shared vectors in `spec/webhook-vectors.json`.

## Regenerate

`pnpm generate` rebuilds `src/generated` from `../spec/openapi.json` (committed). `dist/` is built in CI and on publish.
