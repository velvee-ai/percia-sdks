# Postman collection and Insomnia export

Generated from `spec/openapi.json` by `scripts/generate.mjs`. The three output files are committed; regenerate after every `pnpm spec:sync`:

```bash
node postman/scripts/generate.mjs     # or: pnpm generate (also regenerates the SDKs)
cd postman && npm test                # offline, 9 tests
```

| File | For |
|---|---|
| `percia.postman_collection.json` | Postman, Collection v2.1 (66 requests in 11 folders, plus a 5-step Quickstart folder) |
| `percia.postman_environment.json` | Postman environment `Percia` |
| `percia.insomnia.json` | Insomnia v4 export (same folders, requests and a base environment) |

## Import

- **Postman:** Import both the collection and the environment files, pick the `Percia` environment (top right), set `apiKey` to a key from the dashboard (**API keys**; give it the scopes the folder needs: each request lists them in its description), set `webhookUrl` to the public https address of your receiver (see `../examples`), then open **Quickstart** and send the requests in order.
- **Insomnia:** Application menu, Import, choose `percia.insomnia.json`. Edit the Base Environment: set `apiKey` and `webhookUrl`. Insomnia v4 exports carry no test scripts, so the status-code checks run only in Postman.

## Not in the collection: the dev event feed

`GET /api/events/stream` (Server-Sent Events, for `percia listen`) is deliberately not a request here: Postman and Insomnia buffer or time out on a response that never ends (`x-percia-stream`); the generator skips it. Use `percia listen --print` or `curl --no-buffer -H "Authorization: Bearer $PERCIA_API_KEY" {{baseUrl}}/api/events/stream`; see [`../docs/local-development.md`](../docs/local-development.md).

## Variables

| Variable | Meaning |
|---|---|
| `baseUrl` | Default `https://playground.percia.ai`. Requests go to `{{baseUrl}}/api/...`. |
| `apiKey` | Secret. Sent as `Authorization: Bearer {{apiKey}}` (collection level). Never commit a value. |
| `webhookUrl` | Where watches and hooks deliver. Must be public https. |
| `watchId`, `cameraId`, `whipUrl`, `cameraToken` (secret), `hookId`, `eventId`, `cursor`, `agentId`, `siteId`, `connectionId`, ... | Filled by the test scripts of the create requests (Postman) or by hand. |
| `webhookSecret`, `hookSecret`, `pairUrl`, `connectUrl` | Saved from create responses (they are shown once). Scripts never `console.log` them. Treat `pairUrl` and `connectUrl` as private. |

Scripts save into collection variables, and into the active environment too when one is selected, so an empty environment value never shadows what a script saved.

## What is included

Operations that accept an API key or OAuth token (`bearerAuth` in the spec), plus the open `getHealth`, `getConfig` and `getStatus`. Skipped (29 of 95): session-only routes (`/keys`, `/me`, `/billing/*`, provider keys, claim and manage links, finishing a connect link), device-side camera calls (`/cam/*`), signed-image and callback endpoints, the Stripe and Telegram webhooks, anonymous create and the Better Auth catch-all. The count is printed by the generator.

Every request has a `test` script: the status must be one of the documented success codes, JSON bodies must parse, and any 4xx/5xx must use the shared error envelope (`message`, `error.code`).

> **Do not run the whole collection against a real account.** Delete requests act on the ids saved by earlier requests. Run a folder at a time.

## Design decisions

- **Own generator, not `openapi-to-postmanv2`:** the converter output is not byte-stable across versions, ignores `x-percia-scopes`, cannot build the Quickstart flow or the save-to-variable scripts, and cannot emit Insomnia. About 250 lines of zero-dependency code give deterministic files that CI can diff (`pnpm generate:check`).
- **Offline test:** `test/mock.mjs` answers every documented operation with the spec's example (or a sample from the response schema); `test/runner.mjs` is a minimal Postman-compatible runner that executes the generated test scripts, so the Quickstart, Events feed and REST hooks folders run end to end without Newman or a network. For a real run, use `npx newman run percia.postman_collection.json -e percia.postman_environment.json --folder Quickstart --env-var apiKey=... ` (not run here).
