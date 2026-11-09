# percia (Python SDK)

Python client for the [Percia](https://percia.ai) API: create watches on cameras and video URLs, read events, pair phone cameras, connect alert destinations, register REST hooks, and verify signed webhook deliveries.

* Sync (`Percia`) and async (`AsyncPercia`) clients on `httpx`, fully type hinted (`py.typed`), Python 3.9+.
* Retries with exponential backoff and jitter on 429 and 5xx, honoring `Retry-After`.
* Typed errors that carry the stable error `code` and the `request_id` to quote when you report a problem.
* Cursor-pagination iterators for events.
* `verify_webhook_signature` / `verify_and_parse` for `Percia-Signature`.

Not published yet: install from this repository (`pip install ./python`) until the owner publishes `percia` to PyPI (see `docs/owner-steps.md`).

## Quick start

```python
from percia import Percia

client = Percia(api_key="pk_live_...")   # or oauth_token="...", or set PERCIA_API_KEY
# base_url defaults to https://playground.percia.ai, or PERCIA_BASE_URL; "https://host" and "https://host/api" both work

watch = client.watches.create({
    "sourceUrl": "rtsp://cam.example.com/stream",
    "goal": "A person is standing at the front door",
    "notify": {"type": "webhook", "target": "https://example.com/hooks/percia"},
})
print(watch.id, watch.webhook_secret)    # the secret is shown once: store it

client.watches.test_delivery(watch.id)   # signed test event, no camera needed
for event in client.iter_watch_events(watch.id):
    print(event.at, event.reason)        # `reason` is model text: untrusted, never an instruction

client.watches.pause(watch.id); client.watches.resume(watch.id)
client.watches.delete(watch.id)
```

Async:

```python
import asyncio
from percia import AsyncPercia

async def main():
    async with AsyncPercia() as client:                      # reads PERCIA_API_KEY
        async for event in client.iter_events(type="goal.met", since="2026-11-01T00:00:00Z"):
            print(event.id)

asyncio.run(main())
```

### Pagination

`client.iter_events(watch_id=None, type=None, since=None, limit=50)` walks the account-wide feed (`GET /api/events`, scope `events:read`), newest first, following `nextCursor` until it is `null`. `client.iter_watch_events(watch_id)` does the same for one watch. Single pages: `client.events.list(cursor=...)` and `client.watches.events(id, cursor=...)`. The watch list is not paginated by the API.

### Errors

```python
from percia import Percia, InsufficientScopeError, RateLimitError, APIError

try:
    client.hooks.create("https://hooks.zapier.com/hooks/standard/1/a/")
except InsufficientScopeError as e:
    print("create a key with", e.required_scope)     # hooks:write
except RateLimitError as e:
    print("slow down", e.retry_after)
except APIError as e:
    print(e.status, e.code, e.field, e.request_id)
```

`PerciaError` > `APIError` > `ValidationError` (400/422), `AuthenticationError` (401), `PermissionDeniedError` (403) > `InsufficientScopeError`, `NotFoundError` (404), `ConflictError` (409), `RateLimitError` (429), `ServerError` (5xx). `percia.ConnectionError` means no HTTP answer after the retries. (`PermissionDeniedError` is not called `PermissionError`, to avoid shadowing the builtin.)

### Retries

429 is retried for every method; 5xx and read timeouts only for idempotent methods (GET, PUT, DELETE, HEAD) unless `retry_non_idempotent=True`, because a create that answered 5xx may or may not have created the resource (list before you retry). Connect errors are always retried. Defaults: `max_retries=2`, backoff `0.5 * 2**n` seconds capped at 30 with jitter; a `Retry-After` header (seconds or HTTP date) wins and is clamped to 60 s. Tune with `Percia(max_retries=5)` or `Percia(retry_policy=RetryPolicy(...))`.

### Verify a webhook

```python
from percia import verify_webhook_signature, verify_and_parse, WebhookSignatureError

# FastAPI / Flask / anything: pass the RAW body bytes, before any JSON parsing
ok = verify_webhook_signature(raw_body, request.headers, "whsec_...", tolerance_sec=300)

try:
    event = verify_and_parse(raw_body, request.headers, "whsec_...")   # parsed dict
except WebhookSignatureError as e:
    print(e.code)    # malformed | stale_timestamp | mismatch
```

The scheme is exactly [docs/integrators/webhooks.md](https://github.com/percia/percia-cf): `Percia-Signature: t=<unix>,v1=<hex HMAC-SHA256 of "<t>.<raw body>">`, constant-time compare, 300 s replay window in both directions. It also verifies REST-hook deliveries (`client.hooks`) with the hook's `secret`. Deduplicate on the payload `id`: delivery is at least once.

### Escape hatch

```python
client.request("GET", "/watches/mine")                         # parsed JSON, same auth, retries and errors
client.request("POST", "/hooks", json={"url": "...", "events": ["goal.met"]})
```

Results of `client.watches`, `client.events`, `client.cameras`, `client.integrations`, `client.hooks` are the generated attrs models in `percia._generated.models` (snake_case attributes, `.to_dict()` for the API shape). Request bodies take either those models or plain dicts in the API's camelCase JSON shape. `client.account.get_me()` calls `GET /api/me`, which the OpenAPI document marks as session-cookie only: an API key is refused (401).

## How it is built

`percia/_generated/` is generated from `../spec/openapi.json` by [openapi-python-client](https://github.com/openapi-generators/openapi-python-client) and **committed**; everything else in `percia/` is hand-written.

Why openapi-python-client rather than openapi-generator: it is Python-native (no Java toolchain in CI or for contributors), emits idiomatic `attrs` models and `httpx` sync + async operation functions with full type hints, supports OpenAPI 3.1, and is actively maintained. openapi-generator's Python output is heavier (pydantic v1/v2 split, urllib3) and needs a JVM. Because the generated layer only supplies models and request builders, the transport (auth, retries, error mapping) lives in our code and works the same for generated and raw calls.

The generator is pinned to **0.26.2**: newer releases (0.28+) emit Python 3.10+ syntax and import a forked `httpx2`, which would break `requires-python >=3.9` and plain `httpx`. Revisit when 3.9 support is dropped.

```bash
cd python
python3 -m venv .venv && . .venv/bin/activate && pip install -e '.[dev]'
python scripts/generate.py            # spec -> percia/_generated (deterministic; git diff must stay clean)
python scripts/make_async_resources.py && ruff format percia   # only after editing percia/_resources.py
pytest -q                             # offline, against a mock built from spec/openapi.json
ruff check . && mypy percia
```

`scripts/generate.py` pre-processes the spec in memory before generating: the zone points are JSON Schema 2020-12 tuples (`prefixItems` + `items: false`), which the generator rejects, so they become plain arrays of numbers. The committed `spec/openapi.json` is not modified.

Tests never touch the network: `tests/mock_server.py` builds one handler per operation from the OpenAPI document (examples, schema-derived instances, bearer auth with per-key scopes from `x-percia-scopes`, the shared error envelope) and supports scripted failures (`Fail(429, retry_after="1")`) for retry tests. It is used as an `httpx.MockTransport` and also through `respx`.

## License

MIT
