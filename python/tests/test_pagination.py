from __future__ import annotations

import json

import httpx
import pytest

from percia import AsyncPercia, Percia

from .conftest import KEY


def ev(i: int) -> dict:  # type: ignore[type-arg]
    return {
        "id": f"evt_{i}", "watchId": "w_abc", "decisionId": f"dec_{i}", "occurrenceId": f"occ_{i}", "type": "goal.met",
        "confidence": 0.9, "reason": "r", "at": "2026-11-01T09:30:00.000Z", "deliveryStatus": "delivered", "attempts": 1,
        "concernId": None, "outputs": None, "outputsError": None, "actionResults": None, "integrationResults": [],
        "hasKeyframe": False, "feedback": None, "feedbackNote": None,
    }  # fmt: skip


def paged_handler(total: int, per_page: int, last_empty: bool = False):  # type: ignore[no-untyped-def]
    """Serve `total` events newest first. With last_empty the final real page still names a cursor and the next page is empty."""
    seen = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(dict(request.url.params))
        start = int(request.url.params.get("cursor", "0"))
        limit = min(int(request.url.params.get("limit", "50")), per_page)
        chunk = list(range(start, min(start + limit, total)))
        nxt = start + limit
        more = nxt < total or (last_empty and nxt == total)
        return httpx.Response(200, json={"events": [ev(i) for i in chunk], "nextCursor": str(nxt) if more else None})

    handler.seen = seen  # type: ignore[attr-defined]
    return handler


def test_iter_events_walks_all_pages(client, server):  # type: ignore[no-untyped-def]
    h = paged_handler(7, 3)
    server.on("GET", "/events", h)
    ids = [e.id for e in client.iter_events(limit=3)]
    assert ids == [f"evt_{i}" for i in range(7)]
    assert [s.get("cursor") for s in h.seen] == [None, "3", "6"]  # type: ignore[attr-defined]


def test_iter_events_passes_filters(client, server):  # type: ignore[no-untyped-def]
    h = paged_handler(2, 50)
    server.on("GET", "/events", h)
    list(client.iter_events(watch_id="w_1", type="goal.met", since="2026-11-01T00:00:00Z", limit=100))
    assert h.seen[0] == {"limit": "100", "watchId": "w_1", "type": "goal.met", "since": "2026-11-01T00:00:00Z"}  # type: ignore[attr-defined]


def test_empty_last_page(client, server):  # type: ignore[no-untyped-def]
    h = paged_handler(4, 2, last_empty=True)
    server.on("GET", "/events", h)
    assert len(list(client.iter_events(limit=2))) == 4
    assert len(h.seen) == 3  # type: ignore[attr-defined]


def test_empty_feed(client, server):  # type: ignore[no-untyped-def]
    server.on("GET", "/events", paged_handler(0, 10))
    assert list(client.iter_events()) == []


def test_repeated_cursor_stops(client, server):  # type: ignore[no-untyped-def]
    server.on("GET", "/events", lambda r: httpx.Response(200, json={"events": [ev(1)], "nextCursor": "same"}))
    assert len(list(client.iter_events())) == 2  # first page, the page after "same", then the repeat is detected


def test_iter_is_lazy(client, server):  # type: ignore[no-untyped-def]
    h = paged_handler(100, 10)
    server.on("GET", "/events", h)
    it = client.iter_events(limit=10)
    next(it)
    assert len(h.seen) == 1  # type: ignore[attr-defined]


def test_iter_watch_events(client, server):  # type: ignore[no-untyped-def]
    h = paged_handler(5, 2)
    server.on("GET", "/watches/w_abc/events", h)
    assert [e.id for e in client.iter_watch_events("w_abc", limit=2)] == [f"evt_{i}" for i in range(5)]


def test_iter_watches(client):  # type: ignore[no-untyped-def]
    assert len(list(client.iter_watches())) == 1


def test_event_fields_parse(client, server):  # type: ignore[no-untyped-def]
    server.on("GET", "/events", paged_handler(1, 1))
    e = next(client.iter_events())
    assert (e.watch_id, e.type_, e.delivery_status.value) == ("w_abc", "goal.met", "delivered")


async def test_async_iter_events(aclient, server):  # type: ignore[no-untyped-def]
    h = paged_handler(5, 2, last_empty=True)
    server.on("GET", "/events", h)
    ids = [e.id async for e in aclient.iter_events(limit=2)]
    assert ids == [f"evt_{i}" for i in range(5)]


async def test_async_iter_watch_events_and_watches(aclient, server):  # type: ignore[no-untyped-def]
    server.on("GET", "/watches/w_abc/events", paged_handler(3, 2))
    assert len([e async for e in aclient.iter_watch_events("w_abc", limit=2)]) == 3
    assert len([w async for w in aclient.iter_watches()]) == 1


def test_sync_client_unused_import_guard():
    assert Percia and AsyncPercia and KEY and json
    pytest.importorskip("httpx")
