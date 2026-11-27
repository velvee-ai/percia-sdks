# GitHub Actions examples

| File | What it does |
|---|---|
| `percia-smoke.yml` | Daily (and manual) check of `GET /api/events` for the last 24 hours: fails on any `deliveryStatus: "failed"` event, and on zero events when `require_events` is true. Needs secret `PERCIA_API_KEY` (scope `events:read`). |
| `percia-pr-check.yml` | In a pull request: create a watch, send a signed `test-delivery` to your test receiver, **always delete the watch** (`if: always()`). Needs `watches:write` + `watches:delete`, and variables `PERCIA_TEST_WEBHOOK_URL`, `PERCIA_TEST_SOURCE_URL`. |

Both use `curl` and `jq` (preinstalled on `ubuntu-latest`) so they work today. `percia-smoke.yml` also holds a commented job that does the same with the `percia` CLI (`npx @percia/cli whoami --json`, `events list --json`); the CLI is on npm, so you can enable it.

Notes
- `GET /api/events` is the account-wide feed. Check that your host serves it first: `curl $BASE/api/openapi.json | jq '.paths|has("/events")'` first.
- Use a dedicated key with the fewest scopes, store it as a repository secret, and rotate it from the dashboard. Workflows from forks get no secrets, so the PR check skips them.
- The create response contains `webhookSecret` once; the PR check keeps only the id and removes the file.
