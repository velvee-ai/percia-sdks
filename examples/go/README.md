# Webhook receiver: Go (standard library)

```bash
PERCIA_WEBHOOK_SECRET=whsec_... go run .     # :3000/hooks/percia
go test ./...                                 # offline: 23 tests (20 shared vectors in testdata/vectors.json)
```

`Verify(secret, header, rawBody, now)` is the part to copy; `Receiver` is a ready `http.Handler`.

## How it verifies

`Percia-Signature: t=<unix>,v1=<hex>`; the signed string is `"<t>.<raw body>"`, the key is the whole `whsec_...` secret. The receiver reads the **raw** bytes, rejects timestamps more than 300 s from now, compares the HMAC in constant time, only then parses JSON, answers 2xx fast and skips an `id` it has already handled. `reason` is untrusted model text: it is logged as data and never executed or used as prompt instructions. Contract: `percia-cf/docs/integrators/webhooks.md`.

The shared test vectors (`spec/webhook-vectors.json`, a copy is in this directory) cover valid, stale, mismatch, malformed, unicode and empty-body cases.

## Expose it to Percia

Percia only delivers to public `https` addresses. For local development use a tunnel (for example `cloudflared tunnel --url http://localhost:3000`), then create a watch with `notify: {"type":"webhook","target":"https://<tunnel>/hooks/percia"}` and copy the `webhookSecret` from the create response (shown once) into the environment variable below. Send a signed test event with `POST /api/watches/{id}/test-delivery` (no camera needed).
