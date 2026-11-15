"""The developer event feed iterator (GET /api/events/stream). The mock speaks the SSE contract of percia-cf docs/specs/platform/dev-feed.md."""

from __future__ import annotations

import hashlib
import hmac
import itertools
import json
from typing import Any, Dict, List

import httpx
import pytest

from percia import (
    AsyncPercia,
    AuthenticationError,
    ConnectionError,
    End,
    Event,
    InsufficientScopeError,
    NotFoundError,
    Open,
    Percia,
    Ping,
    Reconnect,
    Resync,
    ServerError,
    ValidationError,
    verify_webhook_signature,
)
from percia._stream import SseParser

from .conftest import KEY


def evt(cursor: int, **over: Any) -> Dict[str, Any]:
    body = {
        "id": f"dec_{cursor}", "watchId": "w_abc", "occurrenceId": f"occ_{cursor}", "type": "goal.met",
        "goal": "A person is at the door", "reason": "A person stands at the door.", "confidence": 0.93,
        "at": "2026-11-14T09:30:00Z", "eventId": f"evt-{cursor}", **over,
    }  # fmt: skip
    return {"id": str(cursor), "body": body}


def message(e: Dict[str, Any]) -> str:
    return f"id: {e['id']}\nevent: {e['body']['type']}\ndata: {json.dumps(e['body'], separators=(',', ':'))}\n\n"


HEAD = "retry: 3000\n: connected\n\n"


def end(reason: str = "max_duration") -> str:
    return f"event: end\ndata: {json.dumps({'reason': reason})}\n\n"


def resync(frm: int) -> str:
    return f"event: resync\ndata: {json.dumps({'reason': 'cursor_too_old', 'from': frm})}\n\n"


def sse(*frames: str) -> httpx.Response:
    return httpx.Response(200, headers={"content-type": "text/event-stream"}, content=(HEAD + "".join(frames)).encode())


def fail(status: int, code: str, msg: str, **headers: str) -> httpx.Response:
    return httpx.Response(
        status, headers=headers, json={"error": {"code": code, "message": msg, "request_id": "req_x"}}
    )


class Feed:
    """Serves the scripted responses in order; records every request."""

    def __init__(self, *responses: httpx.Response) -> None:
        self.responses = list(responses)
        self.requests: List[httpx.Request] = []

    def __call__(self, request: httpx.Request) -> httpx.Response:
        self.requests.append(request)
        # After the script, hold nothing: end the test by raising (a dropped connection), which the tests never reach.
        return self.responses.pop(0) if self.responses else sse()

    def transport(self) -> httpx.MockTransport:
        return httpx.MockTransport(self)


def mk(feed: Feed, **kw: Any) -> Percia:
    return Percia(api_key=KEY, base_url="http://mock.test", transport=feed.transport(), max_retries=0, **kw)


def take(c: Percia, n: int = 1, **kw: Any) -> List[Any]:
    items: List[Any] = []
    stream = c.events.stream(jitter=lambda: 0.5, **kw)
    for it in stream:
        items.append(it)
        if sum(1 for i in items if isinstance(i, Event)) >= n:
            stream.close()
            break
    return items


def test_parser_framing_across_chunks_crlf_bom_and_unicode_separators():
    p = SseParser()
    frames = []
    for chunk in [
        "﻿retry: 3000\r\n: connected\r\n\r\nid: 7\nev",
        'ent: goal.met\ndata: {"a":"x y"}',
        "\n\ndata: a\r",
        "\ndata: b\r\n\r\ndata: tail",
    ]:
        frames += p.feed(chunk)
    assert frames == [
        ("retry", 3000),
        ("comment", "connected"),
        ("message", "7", "goal.met", '{"a":"x y"}'),  # U+2028 is data, not a line end
        ("message", None, "message", "a\nb"),
    ]


def test_connects_with_bearer_and_filters_and_yields_the_exact_data_string(sleeps):  # type: ignore[no-untyped-def]
    e = evt(5)
    feed = Feed(sse(message(e)))
    with mk(feed) as c:
        items = take(c, watch_id="w_abc", type="goal.met", concern_id="c_1", backlog=3)
    assert [i.kind for i in items] == ["open", "event"]
    ev = items[1]
    assert (
        ev.cursor == "5" and ev.data == json.dumps(e["body"], separators=(",", ":")) and ev.event["eventId"] == "evt-5"
    )
    req = feed.requests[0]
    assert req.headers["authorization"] == f"Bearer {KEY}" and req.headers["accept"] == "text/event-stream"
    assert "last-event-id" not in req.headers
    assert dict(req.url.params) == {"watchId": "w_abc", "type": "goal.met", "concernId": "c_1", "backlog": "3"}
    assert req.url.path == "/api/events/stream"


def test_resumes_after_end_with_last_event_id_dedupes_and_uses_the_server_retry(sleeps):  # type: ignore[no-untyped-def]
    feed = Feed(sse(message(evt(5)), message(evt(6)), end()), sse(message(evt(6)), message(evt(7))))
    with mk(feed) as c:
        items = take(c, 3, backlog=2)
    assert [i.cursor for i in items if isinstance(i, Event)] == ["5", "6", "7"]
    assert End("max_duration") in items
    assert any(isinstance(i, Reconnect) and i.reason == "max_duration" and i.delay == 3.0 for i in items)
    assert feed.requests[1].headers["last-event-id"] == "6" and "backlog" not in feed.requests[1].url.params
    assert feed.requests[0].url.params["backlog"] == "2"
    assert sleeps == [3.0]


def test_a_given_cursor_goes_as_since_then_last_event_id(sleeps):  # type: ignore[no-untyped-def]
    feed = Feed(sse(message(evt(9))), sse(message(evt(10))))
    with mk(feed) as c:
        take(c, 2, since=8)
    assert feed.requests[0].url.params["since"] == "8" and "last-event-id" not in feed.requests[0].headers
    assert feed.requests[1].headers["last-event-id"] == "9" and "since" not in feed.requests[1].url.params


def test_resync_and_ping_items(sleeps):  # type: ignore[no-untyped-def]
    feed = Feed(sse(": ping\n\n", resync(3), message(evt(100))))
    with mk(feed) as c:
        items = take(c, since=3)
    assert (
        items[0] == Open(1)
        and Ping() in items
        and Resync("cursor_too_old", "3") in items
        and isinstance(items[-1], Event)
    )


@pytest.mark.parametrize(
    "status,code,exc",
    [
        (401, "invalid_api_key", AuthenticationError),
        (403, "insufficient_scope", InsufficientScopeError),
        (404, "not_found", NotFoundError),
        (400, "invalid_request", ValidationError),
    ],
)
def test_terminal_errors_are_typed_and_not_retried(sleeps, status, code, exc):  # type: ignore[no-untyped-def]
    feed = Feed(fail(status, code, "nope"))
    with mk(feed) as c, pytest.raises(exc):
        next(iter(c.events.stream()))
    assert len(feed.requests) == 1 and sleeps == []


def test_429_waits_retry_after_and_announces_then_connects(sleeps):  # type: ignore[no-untyped-def]
    feed = Feed(fail(429, "rate_limited", "At most 2 streams at once.", **{"retry-after": "5"}), sse(message(evt(1))))
    with mk(feed) as c:
        items = take(c)
    assert isinstance(items[0], Reconnect) and (items[0].reason, items[0].status, items[0].delay, items[0].code) == (
        "rate_limited",
        429,
        5.0,
        "rate_limited",
    )
    assert "2 streams" in (items[0].message or "")
    assert sleeps == [5.0]


def test_5xx_and_network_errors_back_off_with_jitter_and_reset_after_open(sleeps):  # type: ignore[no-untyped-def]
    def boom(request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError("refused", request=request)

    feed = Feed(
        fail(503, "unavailable", "x"), boom, sse(message(evt(1))), fail(503, "unavailable", "x"), sse(message(evt(2)))
    )  # type: ignore[arg-type]
    feed.responses[1] = boom  # type: ignore[assignment]
    calls = itertools.count()

    def handler(request: httpx.Request) -> httpx.Response:
        next(calls)
        r = feed.responses.pop(0)
        feed.requests.append(request)
        return r(request) if callable(r) else r

    with Percia(api_key=KEY, base_url="http://mock.test", transport=httpx.MockTransport(handler), max_retries=0) as c:
        take(c, 2)
    # jitter 0.5: 0.25, 0.5; the closed stream after a successful open waits the server's retry (3 s); then a fresh 0.25
    assert sleeps == [0.25, 0.5, 3.0, 0.25]


def test_max_reconnects_turns_endless_retrying_into_an_error(sleeps):  # type: ignore[no-untyped-def]
    feed = Feed(*[fail(503, "unavailable", "x") for _ in range(3)])
    with mk(feed) as c, pytest.raises(ServerError):
        for _ in c.events.stream(max_reconnects=2):
            pass
    assert len(feed.requests) == 3


def test_a_network_error_is_retried_not_raised_and_can_end_in_connection_error(sleeps):  # type: ignore[no-untyped-def]
    def handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError("refused", request=request)

    with Percia(api_key=KEY, base_url="http://mock.test", transport=httpx.MockTransport(handler), max_retries=0) as c:
        it = c.events.stream(max_reconnects=1)
        first = next(it)
        assert isinstance(first, Reconnect) and first.reason == "network_error"
        with pytest.raises(ConnectionError):
            list(it)


def test_bad_backlog_or_cursor_is_rejected_before_connecting():
    feed = Feed()
    with mk(feed) as c:
        with pytest.raises(ValueError):
            c.events.stream(backlog=21)
        with pytest.raises(ValueError):
            c.events.stream(since="abc")
    assert feed.requests == []


def test_read_timeout_reconnects_as_idle(sleeps):  # type: ignore[no-untyped-def]
    state = {"n": 0}

    def handler(request: httpx.Request) -> httpx.Response:
        state["n"] += 1
        if state["n"] == 1:
            raise httpx.ReadTimeout("silent", request=request)
        return sse(message(evt(1)))

    with Percia(api_key=KEY, base_url="http://mock.test", transport=httpx.MockTransport(handler), max_retries=0) as c:
        items = take(c)
    assert any(isinstance(i, Reconnect) and i.reason == "idle_timeout" for i in items)


def test_signing_what_the_stream_carries_matches_the_documented_algorithm(sleeps):  # type: ignore[no-untyped-def]
    feed = Feed(sse(message(evt(1, reason='quotes "and" unicode é'))))
    with mk(feed) as c:
        ev = [i for i in take(c) if isinstance(i, Event)][0]
    secret, t = "whsec_test_secret", 1_794_000_000
    header = f"t={t},v1=" + hmac.new(secret.encode(), f"{t}.".encode() + ev.data.encode(), hashlib.sha256).hexdigest()
    assert verify_webhook_signature(ev.data, header, secret, now=t + 1)
    assert not verify_webhook_signature(json.dumps(json.loads(ev.data), indent=1), header, secret, now=t)
    assert not verify_webhook_signature(ev.data, header, "whsec_other", now=t)
    assert not verify_webhook_signature(ev.data, header, secret, now=t + 301)


# -- async twin -------------------------------------------------------------------------------------------------


async def test_async_stream_resumes_and_honours_retry_after(sleeps):  # type: ignore[no-untyped-def]
    feed = Feed(
        fail(429, "rate_limited", "At most 2 streams at once.", **{"retry-after": "5"}),
        sse(message(evt(1)), end()),
        sse(message(evt(1)), message(evt(2))),
    )
    async with AsyncPercia(api_key=KEY, base_url="http://mock.test", transport=feed.transport(), max_retries=0) as c:
        items: List[Any] = []
        stream = c.events.stream(jitter=lambda: 0.5)
        async for it in stream:
            items.append(it)
            if sum(1 for i in items if isinstance(i, Event)) == 2:
                await stream.aclose()  # type: ignore[attr-defined]
                break
    assert [i.cursor for i in items if isinstance(i, Event)] == ["1", "2"]
    assert feed.requests[2].headers["last-event-id"] == "1"
    assert sleeps == [5.0, 3.0]


async def test_async_terminal_error(sleeps):  # type: ignore[no-untyped-def]
    feed = Feed(fail(403, "insufficient_scope", "needs events:read"))
    async with AsyncPercia(api_key=KEY, base_url="http://mock.test", transport=feed.transport(), max_retries=0) as c:
        with pytest.raises(InsufficientScopeError):
            async for _ in c.events.stream():
                pass
