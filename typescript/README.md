# @percia/sdk

TypeScript SDK for the [Percia](https://percia.ai) API. Typed, fetch-only (Node 20+, Cloudflare Workers, Deno, Bun, browsers), ESM and CJS.

Install: `npm install @percia/sdk` (<https://www.npmjs.com/package/@percia/sdk>).

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

## Plan, free minutes and how you are charged

Camera-minutes are the real limit (10 free every UTC month, then credit minutes, then the card); plan counts are informational. Check before creating a watch:

```ts
const me = await percia.account.whoami(); // connection test: any valid key or token
const billing = await percia.account.billing(); // the same facts as the `billing` block of MCP whoami
if (!billing.canStartWatches) throw new Error(billing.nextStep ?? "Open the Billing page");
console.log(billing.planLabel, billing.freeMinutesRemaining, billing.creditMinutes, billing.howCharged);
const plan = await percia.account.plan();        // the raw GET /api/plan answer, every API field
```

Every billing field is additive and optional: an older server leaves some out (`billingOf(plan)` gives `null`, never a guess). `describeBilling(billing)` returns plain lines for a person.

## Camera device kind

```ts
await percia.cameras.create("Desk laptop", { deviceKind: "computer" }); // cameras carry deviceKind: phone | tablet | computer | null
```

## Cameras on a private network

```ts
const reg = await percia.cameras.registerPush({ name: "Front door", externalId: "front-door" });
reg.token;      // the publish token, once; on a repeat call { existing: true, token: null } (or onExisting: "rotate" | "throw")
await percia.cameras.rotateToken(reg.camera.id); await percia.cameras.revokeToken(reg.camera.id);
await percia.cameras.status(reg.camera.id);      // { state: waiting | online | offline | revoked, hint, ... }
await percia.cameras.bulk([{ name: "Door", externalId: "nvr1-ch1" }]); // POST /cameras/bulk, up to 10 per request
buildPublishCommands(reg, { rtsp }).ffmpeg;      // uses $PERCIA_CAMERA_TOKEN, never the token
```
See [camera push](../docs/camera-push.md).

## Retries

429 is always retried; 500/502/503/504 and network errors are retried for GET, PUT, DELETE (and any request with an `Idempotency-Key`). A POST or PATCH that failed with 5xx is **not** retried unless `retryNonIdempotent: true`, because the create may have happened. `Retry-After` (seconds or a date) is honored; a wait longer than `maxRetryAfterMs` (60 s) returns the 429 instead. Defaults: `maxRetries: 2`, exponential backoff with full jitter (500 ms base, 8 s cap), 30 s per-attempt timeout.

## Errors

All errors extend `PerciaError`. HTTP failures are `PerciaApiError` (subclasses `AuthenticationError` 401, `PermissionError` 403, `NotFoundError` 404, `ValidationError` 400, `ConflictError` 409, `RateLimitError` 429, `ServerError` 5xx) with `status`, `code`, `field`, `requestId` (quote it in bug reports) and `retryAfterSec`. Connection problems are `PerciaConnectionError` / `PerciaTimeoutError`. Branch on `status` and `code`, never on `message`.

## Pagination

`percia.events.iterate(filters)` and `percia.watches.iterateEvents(id)` are lazy async iterators over `nextCursor`; `break` stops fetching. `percia.events.list()` returns one page.

## Follow the dev event feed (no public URL)

`events.stream()` follows `GET /api/events/stream` (Server-Sent Events, scope `events:read`) for local development and tests. It is an async iterator that reconnects with the last cursor (`Last-Event-ID`), honours `Retry-After`, dedupes on `eventId` and ends when `signal` aborts. It is not a delivery path: webhooks stay the production path.

```ts
const ctl = new AbortController();
for await (const item of client.events.stream({ watchId: "w_...", type: "goal.met", backlog: 5, signal: ctl.signal })) {
  if (item.kind === "event") handle(item.event, item.data); // item.data: the exact JSON string; sign this, not a re-serialisation
  // other kinds: open | resync | end | reconnect | ping
}
```

It throws a typed error for 401/403/404/400 and retries everything else (`maxReconnects` bounds it). `percia listen --forward-to http://localhost:3000/hook` is this plus signing and forwarding; see `docs/local-development.md`.

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
