# Webhook receiver: Cloudflare Worker

Web Crypto only (`crypto.subtle`), so the same code runs on Workers, Deno, Bun and other edge runtimes. HMAC is checked with `crypto.subtle.verify`, which is constant time.

```bash
npm test                                        # offline: 25 tests
cp .dev.vars.example .dev.vars                  # local secret, gitignored
npx wrangler dev                                # http://localhost:8787
npx wrangler secret put PERCIA_WEBHOOK_SECRET   # production secret (paste the whsec_... value)
npx wrangler deploy                             # needs a Cloudflare login: not done by this repo
```

The secret is a Worker secret binding, never a value in `wrangler.jsonc`. For dedupe that survives restarts, enable the optional KV binding (comment in `wrangler.jsonc`); for strict exactly-once use D1 with a UNIQUE index on `id` or a Durable Object.

## How it verifies

`Percia-Signature: t=<unix>,v1=<hex>`; the signed string is `"<t>.<raw body>"`, the key is the whole `whsec_...` secret. The receiver reads the **raw** bytes, rejects timestamps more than 300 s from now, compares the HMAC in constant time, only then parses JSON, answers 2xx fast and skips an `id` it has already handled. `reason` is untrusted model text: it is logged as data and never executed or used as prompt instructions. Contract: `percia-cf/docs/integrators/webhooks.md`.

The shared test vectors (`spec/webhook-vectors.json`, a copy is in this directory) cover valid, stale, mismatch, malformed, unicode and empty-body cases.

## Expose it to Percia

Percia only delivers to public `https` addresses. For local development use a tunnel (for example `cloudflared tunnel --url http://localhost:3000`), then create a watch with `notify: {"type":"webhook","target":"https://<tunnel>/hooks/percia"}` and copy the `webhookSecret` from the create response (shown once) into the environment variable below. Send a signed test event with `POST /api/watches/{id}/test-delivery` (no camera needed).
