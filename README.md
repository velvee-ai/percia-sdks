# percia-sdks

Official SDKs, CLI and OpenAPI spec for the [Percia](https://www.percia.ai) API. Percia 1.0 watches cameras (a phone, a tablet, a computer or any video URL) for a goal you write in plain language and tells you when it is met.

Everything here is generated from one OpenAPI document (`spec/openapi.json`, the same one served at <https://playground.percia.ai/api/openapi.json>) plus a small hand-written layer per language.

**Install**

```bash
npm install @percia/sdk      # TypeScript / JavaScript client
npm install -g @percia/cli   # the `percia` command line
pip install percia           # Python client
```

Packages: [`@percia/sdk`](https://www.npmjs.com/package/@percia/sdk) · [`@percia/cli`](https://www.npmjs.com/package/@percia/cli) · [`percia`](https://pypi.org/project/percia/)

| Directory | What | Package |
|---|---|---|
| [`spec/`](spec) | pinned OpenAPI document, sync + drift check + lint | |
| [`typescript/`](typescript) | typed client, retries, errors, pagination, webhook verification; fetch-only, ESM+CJS | `@percia/sdk` |
| [`python/`](python) | sync + async client, same layer; Python 3.9+, typed | `percia` |
| [`cli/`](cli) | `percia` command line (login, plan, watches, events --follow, cameras, destinations, hooks, listen, mcp setup, doctor) | `@percia/cli` |
| [`postman/`](postman) | Postman collection, environment and Insomnia export | |
| [`examples/`](examples) | webhook receivers (Express, Workers, FastAPI, Go, Ruby), Slack script, Vapi voice alert, GitHub Actions | |
| [`docs/`](docs) | [which tool to use](docs/which-sdk.md), [cameras on a private network](docs/camera-push.md), [receive webhooks without a public URL (`percia listen`)](docs/local-development.md) | |

## Links

- Website: <https://www.percia.ai>
- API docs: <https://playground.percia.ai/docs/>
- Using Percia from a coding agent: <https://playground.percia.ai/coding-agents>
- OpenAPI document: <https://playground.percia.ai/api/openapi.json>
- LLM-readable summary: <https://playground.percia.ai/llms.txt>
- Questions and security reports: support@velvee.ai (see [SECURITY.md](SECURITY.md))

## Quick starts

**TypeScript**
```ts
import { createClient, verifyWebhookSignature } from "@percia/sdk";
const percia = createClient({ apiKey: process.env.PERCIA_API_KEY });
for await (const event of percia.events.iterate({ type: "goal.met" })) console.log(event.at, event.reason);
```

**Python**
```python
import os
from percia import Percia, verify_webhook_signature
percia = Percia(api_key=os.environ["PERCIA_API_KEY"])
for event in percia.iter_events(type="goal.met"):
    print(event.at, event.reason)
```

**CLI**
```bash
percia login && percia watches create --source rtsp://cam.example.com/s --goal "A person is at the door" --webhook https://example.com/hook
percia events list --follow
```

**Webhooks on localhost, no public URL** (dev feed; [guide](docs/local-development.md))
```bash
percia listen --forward-to http://localhost:3000/hook   # PERCIA_WEBHOOK_SECRET signs it like a real delivery
```
```ts
for await (const item of percia.events.stream({ type: "goal.met" })) if (item.kind === "event") console.log(item.event.eventId, item.data);
```
```python
for item in percia.events.stream(type="goal.met"):     # AsyncPercia: async for
    if item.kind == "event": print(item.event["eventId"], item.data)
```

**Camera on a private network** (push; [guide](docs/camera-push.md))
```bash
percia cameras push run --rtsp rtsp://user:pass@192.168.1.20/stream1   # needs ffmpeg 7.1+ with the whip muxer
```
```ts
const reg = await percia.cameras.registerPush({ name: "Front door", externalId: "front-door" }); // reg.token: once
```
```python
reg = percia.cameras.register_push("Front door", "front-door")   # reg.token: once; later calls: token None
```

**Verify a webhook** (any language): header `Percia-Signature: t=<unix>,v1=<hex>`, HMAC-SHA256 of `"<t>.<raw body>"` with the `whsec_...` secret, constant-time compare, reject `|now - t| > 300 s`. Shared test vectors: [`spec/webhook-vectors.json`](spec/webhook-vectors.json).

## Why generate, and with what

One OpenAPI document is the contract; a generated core per language keeps routes, models and `operationId`s in step with the server, and a thin hand-written layer holds what generators do badly (auth, retries, error types, pagination, signature verification).

- **TypeScript: `@hey-api/openapi-ts`** (typed operations + a fetch client with an injectable `fetch`) rather than `openapi-typescript` + `openapi-fetch`: the document carries stable `operationId`s for named SDK functions, and hey-api emits those, the request/response types and error unions in one pass. `openapi-fetch` is smaller and steadier but is path-keyed rather than operation-named, and we would hand-write every wrapper. Cost: hey-api is 0.x and renames things between releases, so the version is pinned and the output is committed.
- **Python: `openapi-python-client`** (attrs models, httpx sync + async, no Java) rather than OpenAPI Generator's Python target (heavier toolchain, less idiomatic typing). Pinned at 0.26.2: later versions emit Python 3.10+ syntax and depend on a forked httpx.
- Hosted generators (Stainless, Speakeasy, Fern) are an option later; the spec-first setup makes switching possible.

## Committed vs built in CI

| | Committed | Built in CI / on publish |
|---|---|---|
| `spec/openapi.json`, `spec.lock.json` | yes | |
| `typescript/src/generated/` (hey-api output) | yes | CI regenerates and fails on any diff (`pnpm generate:check`) |
| `python/percia/_generated/` (openapi-python-client output) | yes (the sdist/wheel need it, no network at install) | same diff check |
| `postman/*.json` (collection, environment, Insomnia) | yes | same diff check |
| `typescript/dist`, `cli/dist` | no | `pnpm build` in CI; `prepublishOnly` on publish |
| Python wheel/sdist | no | `python -m build` in the release workflow |

## Develop

```bash
pnpm install
pnpm test                # sdk + cli (vitest), offline against a mock server built from the spec
cd python && python3 -m venv .venv && . .venv/bin/activate && pip install -e ".[dev]" && pytest -q
node postman/scripts/generate.mjs && (cd postman && npm test)
pnpm generate            # after pnpm spec:sync; needs openapi-python-client on PATH
```

All tests run offline. No real credentials are used anywhere; the mock servers answer from the document's examples and check Bearer keys and scopes (`x-percia-scopes`).

## Contributing and license

See [CONTRIBUTING.md](CONTRIBUTING.md). Report vulnerabilities as described in [SECURITY.md](SECURITY.md). MIT licensed, Copyright (c) 2026 Velvee, Inc.
