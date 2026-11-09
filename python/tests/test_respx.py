"""The same spec-derived mock, mounted with respx on the real httpx transport (no custom transport passed)."""

from __future__ import annotations

import httpx
import respx

from percia import AsyncPercia, Percia

from .conftest import KEY
from .mock_server import Fail, MockPercia


def test_respx_sync(sleeps):  # type: ignore[no-untyped-def]
    server = MockPercia()
    server.script("GET", "/watches/mine", [Fail(429, retry_after="1")])
    with respx.mock(assert_all_called=False) as router:
        router.route(host="api.percia.test").mock(side_effect=server.handler)
        with Percia(api_key=KEY, base_url="https://api.percia.test") as c:
            assert c.watches.list()
    assert sleeps == [1.0]
    assert server.requests[0].url.host == "api.percia.test"


async def test_respx_async(sleeps):  # type: ignore[no-untyped-def]
    server = MockPercia()
    with respx.mock() as router:
        router.route(host="api.percia.test").mock(side_effect=server.handler)
        async with AsyncPercia(api_key=KEY, base_url="https://api.percia.test/api") as c:
            assert (await c.events.sample()).events
    assert server.requests[0].url.path == "/api/events/sample"


def test_respx_plain_route_without_the_server(sleeps):  # type: ignore[no-untyped-def]
    with respx.mock() as router:
        router.get("https://x.test/api/watches/mine").mock(return_value=httpx.Response(200, json=[]))
        with Percia(api_key=KEY, base_url="https://x.test") as c:
            assert c.watches.list() == []
