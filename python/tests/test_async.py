from __future__ import annotations

import httpx
import pytest

from percia import AsyncPercia, AuthenticationError, ConnectionError, InsufficientScopeError, RateLimitError

from .conftest import KEY
from .mock_server import Fail, Json


async def test_async_quickstart(aclient, server):  # type: ignore[no-untyped-def]
    w = await aclient.watches.create(
        {
            "sourceUrl": "rtsp://cam.example.com/s",
            "goal": "A person at the door",
            "notify": {"type": "webhook", "target": "https://example.com/h"},
        }
    )
    assert w.id
    assert (await aclient.watches.get(w.id)).id
    assert (await aclient.watches.events(w.id)).events
    await aclient.watches.pause(w.id)
    await aclient.watches.delete(w.id)
    assert server.requests[-1].headers["authorization"] == f"Bearer {KEY}"


async def test_async_other_resources(aclient):  # type: ignore[no-untyped-def]
    assert (await aclient.cameras.create("Hall")).pair_url
    assert await aclient.hooks.list()
    assert (await aclient.hooks.create("https://example.com/h")).secret
    assert (await aclient.events.sample()).events
    assert (await aclient.integrations.connect("slack")).connect_url
    assert await aclient.request("GET", "/watches/mine")


async def test_async_whoami(aclient, server):  # type: ignore[no-untyped-def]
    server.script("GET", "/whoami", [Json({"userId": "u1", "credential": "session", "scopes": None, "email": "a@b.co"})])
    who = await aclient.account.whoami()
    assert (who.user_id, who.credential, who.scopes, who.email) == ("u1", "session", None, "a@b.co")


async def test_async_retry_after(aclient, server, sleeps):  # type: ignore[no-untyped-def]
    server.script("GET", "/watches/mine", [Fail(429, retry_after="2"), Json([])])
    assert await aclient.watches.list() == []
    assert sleeps == [2.0]


async def test_async_5xx_backoff_and_give_up(aclient, server, sleeps):  # type: ignore[no-untyped-def]
    server.script("GET", "/watches/mine", [Fail(503)] * 5)
    with pytest.raises(Exception) as exc:  # noqa: B017
        await aclient.watches.list()
    assert exc.value.status == 503  # type: ignore[attr-defined]
    assert len(sleeps) == 2 and len(server.calls("GET", "/watches/mine")) == 3


async def test_async_post_5xx_not_retried(aclient, server, sleeps):  # type: ignore[no-untyped-def]
    server.script("POST", "/cameras", [Fail(503)])
    with pytest.raises(Exception):  # noqa: B017
        await aclient.cameras.create("x")
    assert sleeps == []


async def test_async_errors(server, sleeps):  # type: ignore[no-untyped-def]
    server.keys["ro"] = ["watches:read"]
    async with AsyncPercia(api_key="nope", base_url="http://mock.test", transport=server.transport()) as c:
        with pytest.raises(AuthenticationError):
            await c.watches.list()
    async with AsyncPercia(api_key="ro", base_url="http://mock.test", transport=server.transport()) as c:
        with pytest.raises(InsufficientScopeError) as exc:
            await c.hooks.list()
        assert exc.value.request_id
    server.script("GET", "/watches/mine", [Fail(429, retry_after="1")] * 3)
    async with AsyncPercia(api_key=KEY, base_url="http://mock.test", transport=server.transport(), max_retries=0) as c:
        with pytest.raises(RateLimitError) as exc2:
            await c.watches.list()
        assert exc2.value.retry_after == 1.0


async def test_async_connection_error(server, sleeps):  # type: ignore[no-untyped-def]
    server.script("GET", "/watches/mine", [httpx.ConnectError("x")] * 4)
    async with AsyncPercia(api_key=KEY, base_url="http://mock.test", transport=server.transport()) as c:
        with pytest.raises(ConnectionError):
            await c.watches.list()
    assert len(sleeps) == 2


async def test_async_context_closes(server):  # type: ignore[no-untyped-def]
    async with AsyncPercia(api_key=KEY, base_url="http://mock.test", transport=server.transport()) as c:
        pass
    assert c._http.is_closed
