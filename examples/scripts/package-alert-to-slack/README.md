# Package alert to Slack

Two ways to get "a package was left at the door" into Slack.

## A. Percia's native Slack connection (no code, recommended)

Slack is a first-party destination, with retries and signing handled for you.

```bash
BASE=https://playground.percia.ai   # your Percia host
# 1. Ask for a connect link (scope integrations:write). A person opens it while signed in and approves Slack.
curl -sS -X POST "$BASE/api/integrations/connect" -H "Authorization: Bearer $PERCIA_API_KEY" \
  -H 'content-type: application/json' -d '{"service":"slack"}'      # -> {"connectUrl": "...", "expiresAt": "..."}
# 2. After they finish, list connections (scope integrations:read) and take the Slack connection id
curl -sS "$BASE/api/integrations" -H "Authorization: Bearer $PERCIA_API_KEY"
# 3. Create the watch, then attach the connection with a rule (on "*" = every event)
curl -sS -X PUT "$BASE/api/watches/$WATCH_ID/integrations" -H "Authorization: Bearer $PERCIA_API_KEY" \
  -H 'content-type: application/json' -d '{"rules":[{"connectionId":"'$CONNECTION_ID'","on":"*"}]}'
```

A connection created with `"default": true` is attached to every new watch automatically. The connect link is single use and private: treat it like a password.

## B. This script: your own receiver forwards to a Slack incoming webhook

Use it when you want to change the message, filter, or add routing of your own.

```bash
cp .env.example .env      # fill in; export the variables (or use your shell's dotenv)
node create-watch.mjs     # creates the watch; the signing secret is saved to .percia-webhook-secret (0600), not printed
export PERCIA_WEBHOOK_SECRET=$(cat .percia-webhook-secret)
node receiver.mjs         # :3000/hooks/percia  (expose it publicly with a tunnel for Percia to reach it)
npm test                  # offline: 5 tests (message format, escaping, receiver)
```

What it does with a delivery: verifies the signature over the raw body (`verify.mjs`, 300 s tolerance), drops repeated ids, answers 2xx, then posts a Block Kit message built by `formatSlackMessage`. `reason` is model text about camera content, so it is escaped (`&`, `<`, `>`), clipped to 300 characters and shown as a quote, never interpreted. The keyframe link (`imageUrl`, private and non-expiring) is left out unless `INCLUDE_IMAGE=1`, and the receiver never logs it or the secret.

Without `WEBHOOK_TARGET`, `create-watch.mjs` omits `notify`: alerts then email the account owner, and you can attach Slack with option A.
