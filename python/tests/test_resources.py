from __future__ import annotations

import httpx
import pytest

from percia import AuthenticationError, InsufficientScopeError, Percia, ValidationError, billing_of, describe_billing

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


PLAN = {
    "plan": "free",
    "label": "Free",
    "billingEnforced": True,
    "paid": False,
    "hasCard": False,
    "freeMinutes": 10,
    "freeMinutesLeft": 4,
    "creditMinutes": 20,
    "minutesUsedThisMonth": 6,
    "freeMinutesResetsAt": "2026-12-01T00:00:00.000Z",
    "canStartWatches": True,
    "blockReason": None,
    "howCharged": "Charged by the exact camera-minute.",
    "nextStep": "Add a card for 50 more free minutes.",
    "bonusAvailable": True,
    "bonusMinutes": 50,
    "payment": {"state": "active", "billingUrl": "https://percia.test/billing"},
}


def test_billing_block_from_plan(client, server):  # type: ignore[no-untyped-def]
    import httpx

    server.on("GET", "/plan", lambda req: httpx.Response(200, json=PLAN))
    b = client.account.billing()
    assert (b.plan_label, b.free_minutes_remaining, b.credit_minutes, b.minutes_used_this_month) == ("Free", 4, 20, 6)
    assert b.can_start_watches and b.bonus_available and b.bonus_minutes == 50
    assert b.billing_url == "https://percia.test/billing" and b.payment_state == "active"
    text = "\n".join(describe_billing(b))
    assert "4 left this month" in text and "Credit:        20 minutes" in text and "Next step:" in text


def test_billing_of_old_plan_and_blocked():
    old = billing_of({"plan": "free"})
    assert (
        old.plan_label is None
        and old.free_minutes_remaining is None
        and old.can_start_watches
        and not old.bonus_available
    )
    blocked = billing_of(
        {**PLAN, "canStartWatches": False, "blockReason": "needs_billing", "payment": {"state": "blocked"}}
    )
    assert not blocked.can_start_watches
    assert "blocked (needs_billing)" in "\n".join(describe_billing(blocked))


def test_create_watch_interpretation_options(client, server):  # type: ignore[no-untyped-def]
    import json

    client.watches.create(
        {
            "sourceUrl": "rtsp://cam.example.com/s",
            "goal": "A car pulls in",
            "interpret": False,
            "kind": "event",
            "notify": {"type": "email", "target": "a@b.co"},
        }
    )
    assert json.loads(server.requests[-1].read())["interpret"] is False
    client.watches.create(
        {
            "sourceUrl": "rtsp://cam.example.com/s",
            "goal": "Front door",
            "concerns": [{"text": "A person stands at the door", "kind": "state", "ignore": ["the cat"]}],
            "notify": {"type": "email", "target": "a@b.co"},
        }
    )
    assert json.loads(server.requests[-1].read())["concerns"][0]["kind"] == "state"


def test_interpret_and_reinterpret(client, server):  # type: ignore[no-untyped-def]
    import json

    assert client.watches.interpret("Tell me when a car pulls in") is not None
    assert json.loads(server.requests[-1].read()) == {"goal": "Tell me when a car pulls in"}
    client.watches.reinterpret("w_1")
    assert server.requests[-1].url.path.endswith("/watches/w_1/reinterpret")


def test_camera_device_kind(client, server):  # type: ignore[no-untyped-def]
    import json

    client.cameras.create("Hall")
    assert json.loads(server.requests[-1].read()) == {"name": "Hall"}
    client.cameras.create("Desk", device_kind="computer")
    assert json.loads(server.requests[-1].read()) == {"name": "Desk", "deviceKind": "computer"}
