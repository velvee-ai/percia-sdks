# Examples

Runnable templates. Each directory is standalone (copy it out); every test runs offline.

| Directory | What | Tests |
|---|---|---|
| `node-express/` | Webhook receiver, Express, raw-body verification, dedupe | `npm test`: 25 |
| `cloudflare-worker/` | Webhook receiver as a Worker (Web Crypto, optional KV dedupe) | `npm test`: 25 |
| `python-fastapi/` | Webhook receiver, FastAPI, stdlib verification | `pytest`: 23 |
| `go/` | Webhook receiver, standard library | `go test ./...`: 23 |
| `ruby/` | Verifier (OpenSSL) and a tiny WEBrick receiver | `ruby test/percia_verify_test.rb`: 22 |
| `scripts/package-alert-to-slack/` | Create a "package at the door" watch, forward alerts to Slack (and the native Slack alternative) | `npm test`: 5 |
| `vapi-voice-alert/` | Documentation: webhook to a Vapi outbound phone call, with guardrails (placeholders, not run) | none |
| `github-actions/` | Scheduled smoke check and an ephemeral-watch PR check | YAML parse only |

The five verifiers pass the same 20 cases in `spec/webhook-vectors.json` (valid, 299 s skew, unicode and empty bodies, spaces in the header, stale, wrong secret, tampered body, trailing newline, altered timestamp, uppercase hex, missing/garbage header). The rule they implement: `HMAC-SHA256(secret, "<t>.<raw body>")` as lowercase hex, `|now - t| <= 300`, constant-time compare, then parse. Contract: `percia-cf/docs/integrators/webhooks.md`.

Never put a real `pk_live_...` key or `whsec_...` secret in these files; `.env.example` files hold placeholders only.
