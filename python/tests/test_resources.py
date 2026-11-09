from __future__ import annotations

import httpx
import pytest

from percia import AuthenticationError, InsufficientScopeError, Percia, ValidationError

from .conftest import KEY


def test_quickstart_flow(client, server):  # type: ignore[no-untyped-def]
    watch = client.watches.create(
        {
            "sourceUrl": "rtsp://cam.example.com/stream",
            "goal": "A person is standing at the front door",
            "notify": {"type": "webhook", "target": "https://example.com/hooks/percia"},
        }
    )
    assert watch.id and watch.status
    body = server.requests[-1].read()
    assert (
        b'"sourceUrl":"rtsp://cam.example.com/stream"' in body.replace(b" ", b"")
        and server.requests[-1].method == "POST"
    )
    assert server.requests[-1].url.path == "/api/watches/owned"

    got = client.watches.get(watch.id)
    assert got.id
    assert client.watches.test_delivery(watch.id) is not None
    page = client.watches.events(watch.id, limit=20)
    assert page.events and server.requests[-1].url.params["limit"] == "20"
    assert client.watches.delete(watch.id) is not None
    assert server.requests[-1].method == "DELETE"


def test_pause_resume_send_status(client, server):  # type: ignore[no-untyped-def]
    client.watches.pause("w_1")
    assert server.requests[-1].method == "PATCH" and server.requests[-1].read() == b'{"status":"paused"}'
    client.watches.resume("w_1")
    assert server.requests[-1].read() == b'{"status":"active"}'


def test_rotate_secret_and_list(client, server):  # type: ignore[no-untyped-def]
    assert client.watches.rotate_secret("w_1") is not None
    assert server.requests[-1].url.path == "/api/watches/w_1/secret/rotate"
    assert isinstance(client.watches.list(), list)


def test_update_accepts_generated_model(client, server):  # type: ignore[no-untyped-def]
    from percia._generated.models.update_watch_body import UpdateWatchBody

    client.watches.update("w_1", UpdateWatchBody.from_dict({"goal": "A package is on the porch"}))
    assert b"A package is on the porch" in server.requests[-1].read()


def test_missing_scope_blocks_writes(server, sleeps):  # type: ignore[no-untyped-def]
    server.keys["pk_live_ro"] = ["watches:read", "events:read"]
    with Percia(api_key="pk_live_ro", base_url="http://mock.test", transport=server.transport()) as c:
        assert c.watches.list() is not None
        with pytest.raises(InsufficientScopeError) as exc:
            c.watches.create({"sourceUrl": "rtsp://a.example.com/s", "goal": "A person at the door"})
    assert exc.value.required_scope == "watches:write"


def test_create_validation_error_from_server(client):  # type: ignore[no-untyped-def]
    with pytest.raises(ValidationError) as exc:
        client.request("POST", "/cameras", json={"nickname": "x"})
    assert exc.value.field == "name"


def test_account_events_filters(client, server):  # type: ignore[no-untyped-def]
    client.events.list(limit=10, watch_id="w_1", type="goal.met", since=1793525400)
    q = server.requests[-1].url.params
    assert (q["limit"], q["watchId"], q["type"], q["since"]) == ("10", "w_1", "goal.met", "1793525400")
    import datetime as dt

    client.events.list(since=dt.datetime(2026, 11, 1, tzinfo=dt.timezone.utc))
    assert server.requests[-1].url.params["since"] == "2026-11-01T00:00:00+00:00"


def test_sample_event(client):  # type: ignore[no-untyped-def]
    page = client.events.sample()
    assert page.events and page.events[0].id


def test_hooks_lifecycle(client, server):  # type: ignore[no-untyped-def]
    created = client.hooks.create("https://hooks.zapier.com/hooks/standard/1/a/", ["goal.met"], label="Zap")
    assert created.secret.startswith("whsec_")
    sent = httpx.Request("POST", "http://x", content=server.requests[-1].read())
    assert b'"label":"Zap"' in sent.content.replace(b" ", b"")
    assert client.hooks.list()
    assert client.hooks.test("hk_1") is not None
    assert client.hooks.delete("hk_1") is not None


def test_hook_default_event_and_watch(client, server):  # type: ignore[no-untyped-def]
    client.hooks.create("https://example.com/h", watch_id="w_9")
    body = server.requests[-1].read().replace(b" ", b"")
    assert b'"events":["goal.met"]' in body and b'"watchId":"w_9"' in body


def test_cameras(client, server):  # type: ignore[no-untyped-def]
    cam = client.cameras.create("Hall phone")
    assert cam.pair_url
    assert client.cameras.list()
    assert client.cameras.pair("cam_1").pair_url
    client.cameras.delete("cam_1")
    assert server.requests[-1].method == "DELETE"


def test_integrations(client, server):  # type: ignore[no-untyped-def]
    link = client.integrations.connect("slack")
    assert link.connect_url
    assert client.integrations.services() is not None and client.integrations.list() is not None
    assert client.integrations.watch_rules("w_1") is not None
    client.integrations.set_watch_rules("w_1", {"rules": [{"connectionId": "c_1", "on": "*"}]})
    assert b"connectionId" in server.requests[-1].read()
    client.integrations.delete("c_1")


def test_account_get_me_is_session_only(client):  # type: ignore[no-untyped-def]
    # The spec lists /me as session-cookie only: an API key is refused (the mock mirrors that).
    with pytest.raises(AuthenticationError):
        client.account.get_me()


def test_key_with_default_scopes_cannot_use_hooks(server, sleeps):  # type: ignore[no-untyped-def]
    server.keys["pk_live_default"] = ["watches:read", "watches:write", "events:read"]
    with Percia(api_key="pk_live_default", base_url="http://mock.test", transport=server.transport()) as c:
        with pytest.raises(InsufficientScopeError):
            c.hooks.create("https://example.com/h")
    assert KEY != "pk_live_default"
