from __future__ import annotations

import json
from pathlib import Path

import pytest

from percia import (
    ConflictError,
    NotFoundError,
    Percia,
    PerciaError,
    RateLimitError,
    build_publish_commands,
    publish_argv,
    scrub_token,
)
from percia._push import TOKEN_PLACEHOLDER

from .conftest import KEY
from .mock_server import Fail, Json, MockPercia

CONTRACT = json.loads((Path(__file__).resolve().parents[2] / "spec" / "camera-push-contract.json").read_text())
CREATED = CONTRACT["register"]["created"]
EXISTING = CONTRACT["register"]["existing"]
ROTATE = CONTRACT["rotate"]
TOKEN = CREATED["body"]["token"]
WHIP = CREATED["body"]["whipUrl"]


def mk(server: MockPercia, **kw):  # type: ignore[no-untyped-def]
    return Percia(api_key=KEY, base_url="http://mock.test", transport=server.transport(), max_retries=0, **kw)


def test_register_creates_and_returns_the_one_time_token(server):  # type: ignore[no-untyped-def]
    server.script("POST", "/cameras", [Json(CREATED["body"], 201)])
    with mk(server) as c:
        reg = c.cameras.register_push("Hall camera", "lan-cam-1")
    assert json.loads(server.requests[0].read()) == CONTRACT["register"]["request"]
    assert (reg.existing, reg.rotated, reg.token, reg.whip_url) == (False, False, TOKEN, WHIP)
    assert reg.camera.kind.value == "push"
    assert reg.publish and "ffmpegCopy" in reg.publish


def test_repr_never_shows_the_token(server):  # type: ignore[no-untyped-def]
    server.script("POST", "/cameras", [Json(CREATED["body"], 201)])
    with mk(server) as c:
        reg = c.cameras.register_push("Hall camera", "lan-cam-1")
    assert TOKEN not in repr(reg) and TOKEN not in str(reg) and "<hidden>" in repr(reg)


def test_idempotent_200_has_no_token(server):  # type: ignore[no-untyped-def]
    server.script("POST", "/cameras", [Json(EXISTING["body"], 200)])
    with mk(server) as c:
        reg = c.cameras.register_push("Hall camera", "lan-cam-1")
    assert (reg.existing, reg.token, reg.rotated) == (True, None, False)
    assert len(server.requests) == 1


def test_on_existing_rotate_mints_a_new_token(server):  # type: ignore[no-untyped-def]
    server.script("POST", "/cameras", [Json(EXISTING["body"], 200)])
    server.script("POST", "/cameras/cam_push_1/token", [Json(ROTATE["body"], 200)])
    with mk(server) as c:
        reg = c.cameras.register_push("Hall camera", "lan-cam-1", on_existing="rotate")
    assert (reg.existing, reg.rotated, reg.token) == (True, True, ROTATE["body"]["token"])


def test_on_existing_throw_names_rotate_token(server):  # type: ignore[no-untyped-def]
    server.script("POST", "/cameras", [Json(EXISTING["body"], 200)])
    with mk(server) as c, pytest.raises(PerciaError) as exc:
        c.cameras.register_push("n", "lan-cam-1", on_existing="throw")
    assert "rotate_token" in str(exc.value) and "pc_" not in str(exc.value)


def test_errors_carry_the_code(server):  # type: ignore[no-untyped-def]
    server.script("POST", "/cameras", [Fail(429, code="camera_limit")])
    with mk(server) as c, pytest.raises(RateLimitError) as exc:
        c.cameras.register_push("n", "x")
    assert exc.value.code == "camera_limit"


def test_server_without_push_support_is_refused(server):  # type: ignore[no-untyped-def]
    server.script("POST", "/cameras", [Json({"camera": {"id": "c"}, "pairUrl": "https://x"}, 201)])
    with mk(server) as c, pytest.raises(PerciaError, match="whipUrl"):
        c.cameras.register_push("n", "x")


def test_rotate_revoke_and_wrong_kind(server):  # type: ignore[no-untyped-def]
    server.script("POST", "/cameras/cam_push_1/token", [Json(ROTATE["body"], 200)])
    server.script("DELETE", "/cameras/cam_phone/token", [Fail(409, code="wrong_kind")])
    with mk(server) as c:
        assert c.cameras.rotate_token("cam_push_1").token == ROTATE["body"]["token"]
        c.cameras.revoke_token("cam_push_1")
        with pytest.raises(ConflictError) as exc:
            c.cameras.revoke_token("cam_phone")
    assert exc.value.code == "wrong_kind"
    assert [(r.method, r.url.path) for r in server.requests[:2]] == [
        ("POST", "/api/cameras/cam_push_1/token"),
        ("DELETE", "/api/cameras/cam_push_1/token"),
    ]


def test_rotate_needs_watches_delete(server):  # type: ignore[no-untyped-def]
    server.keys["pk_live_limited"] = ["cameras:write"]
    with Percia(api_key="pk_live_limited", base_url="http://mock.test", transport=server.transport()) as c:
        with pytest.raises(Exception) as exc:
            c.cameras.rotate_token("cam_push_1")
    assert getattr(exc.value, "status", None) == 403 and exc.value.code == "insufficient_scope"  # type: ignore[attr-defined]


STATUS = CONTRACT["status"]
BULK = CONTRACT["bulk"]
BULK_ITEMS = [{"name": c["name"], "external_id": c["externalId"]} for c in BULK["request"]["cameras"]]


def test_status_calls_the_status_route(server):  # type: ignore[no-untyped-def]
    server.script("GET", "/cameras/cam_push_1/status", [Json(STATUS["online"]["body"])])
    with mk(server) as c:
        st = c.cameras.status("cam_push_1")
    assert (st.id, st.state, st.status, st.kind, st.seconds_since_seen, st.watch_count, st.hint, st.derived) == (
        "cam_push_1", "online", "online", "push", 12, 1, "Receiving video.", False
    )  # fmt: skip
    assert [r.url.path for r in server.requests] == ["/api/cameras/cam_push_1/status"]


def test_status_revoked_and_waiting_pass_through(server):  # type: ignore[no-untyped-def]
    server.script(
        "GET", "/cameras/cam_push_1/status", [Json(STATUS["revoked"]["body"]), Json(STATUS["waiting"]["body"])]
    )
    with mk(server) as c:
        assert c.cameras.status("cam_push_1").state == "revoked"
        waiting = c.cameras.status("cam_push_1")
    assert (waiting.state, waiting.last_seen_at, waiting.seconds_since_seen) == ("waiting", None, None)


def test_status_falls_back_to_the_list_on_404(server):  # type: ignore[no-untyped-def]
    server.script("GET", "/cameras/cam_push_1/status", [Fail(404, code="not_found")])
    server.script("GET", "/cameras", [Json([EXISTING["body"]["camera"]])])
    with mk(server) as c:
        st = c.cameras.status("cam_push_1")
    assert (st.derived, st.state, st.status, st.kind, st.watch_count, st.hint, st.name) == (
        True, "online", "online", "push", 1, None, "Hall camera"
    )  # fmt: skip
    assert [r.url.path for r in server.requests] == ["/api/cameras/cam_push_1/status", "/api/cameras"]


def test_status_unknown_camera_is_not_found(server):  # type: ignore[no-untyped-def]
    server.script("GET", "/cameras/nope/status", [Fail(404, code="not_found")])
    server.script("GET", "/cameras", [Json([])])
    with mk(server) as c:
        with pytest.raises(NotFoundError):
            c.cameras.status("nope")


def test_status_other_errors_do_not_fall_back(server):  # type: ignore[no-untyped-def]
    server.script("GET", "/cameras/cam_push_1/status", [Fail(403, code="insufficient_scope")])
    with mk(server) as c:
        with pytest.raises(Exception) as exc:
            c.cameras.status("cam_push_1")
    assert exc.value.code == "insufficient_scope" and len(server.requests) == 1  # type: ignore[attr-defined]


def test_bulk_is_one_request_and_keeps_order(server):  # type: ignore[no-untyped-def]
    server.script("POST", "/cameras/bulk", [Json(BULK["created"]["body"], 201)])
    with mk(server) as c:
        res = c.cameras.bulk(BULK_ITEMS)
    assert len(server.requests) == 1 and json.loads(server.requests[0].read()) == BULK["request"]
    assert [(r["external_id"], r["ok"]) for r in res] == [("a", True), ("b", True)]
    a, b = res[0]["registration"], res[1]["registration"]
    assert (a.existing, a.token, b.existing, b.token) == (False, "pc_FAKE_TOKEN_bulk_a_0003", True, None)
    assert a.camera.id == "cam_push_1" and "pc_FAKE" not in repr(a)


def test_bulk_all_existing_200_still_has_a_body(server):  # type: ignore[no-untyped-def]
    server.script("POST", "/cameras/bulk", [Json(BULK["allExisting"]["body"], 200)])
    with mk(server) as c:
        res = c.cameras.bulk(BULK_ITEMS)
    assert [r["registration"].existing for r in res] == [True, True]
    assert [r["registration"].token for r in res] == [None, None]


def test_bulk_on_existing_rotate_and_throw(server):  # type: ignore[no-untyped-def]
    server.script("POST", "/cameras/bulk", [Json(BULK["created"]["body"], 201), Json(BULK["created"]["body"], 201)])
    server.script("POST", "/cameras/cam_push_2/token", [Json(ROTATE["body"])])
    with mk(server) as c:
        rotated = c.cameras.bulk(BULK_ITEMS, on_existing="rotate")
        thrown = c.cameras.bulk(BULK_ITEMS, on_existing="throw")
    assert rotated[1]["registration"].rotated and rotated[1]["registration"].token == ROTATE["body"]["token"]
    assert [r["ok"] for r in thrown] == [True, False]


def test_bulk_chunks_of_ten(server):  # type: ignore[no-untyped-def]
    import httpx

    def handler(req: httpx.Request) -> httpx.Response:
        cams = json.loads(req.read())["cameras"]
        return httpx.Response(
            201,
            json={
                "cameras": [
                    {"camera": {"id": f"c_{x['externalId']}", "name": x["name"], "kind": "push", "externalId": x["externalId"]},
                     "whipUrl": "https://m/whip", "token": f"pc_{i}"}
                    for i, x in enumerate(cams)
                ]
            },
        )  # fmt: skip

    server.on("POST", "/cameras/bulk", handler)
    items = [{"name": f"n{i}", "external_id": f"id{i}"} for i in range(12)]
    with mk(server) as c:
        res = c.cameras.bulk(items)
    assert [len(json.loads(r.read())["cameras"]) for r in server.requests] == [10, 2]
    assert [r["external_id"] for r in res] == [i["external_id"] for i in items] and all(r["ok"] for r in res)


def test_bulk_camera_limit_is_reported_on_every_item_of_the_chunk(server):  # type: ignore[no-untyped-def]
    server.script("POST", "/cameras/bulk", [Fail(429, code="camera_limit")])
    with mk(server) as c:
        res = c.cameras.bulk(BULK_ITEMS)
    assert [r["ok"] for r in res] == [False, False] and res[0]["error"].code == "camera_limit"
    assert len(server.requests) == 1


def test_bulk_falls_back_to_per_item_registration_on_404(server):  # type: ignore[no-untyped-def]
    import httpx

    server.script("POST", "/cameras/bulk", [Fail(404, code="not_found")])

    def handler(req: httpx.Request) -> httpx.Response:
        ext = json.loads(req.read())["externalId"]
        if ext == "bad":
            return httpx.Response(429, json={"error": {"code": "camera_limit", "message": "limit"}})
        body = {**CREATED["body"], "camera": {**CREATED["body"]["camera"], "externalId": ext}}
        return httpx.Response(201, json=body)

    server.on("POST", "/cameras", handler)
    with mk(server) as c:
        res = c.cameras.bulk(
            [{"name": "a", "external_id": "a"}, {"name": "b", "external_id": "bad"}, {"name": "c", "external_id": "c"}]
        )
    assert [(r["external_id"], r["ok"]) for r in res] == [("a", True), ("bad", False), ("c", True)]
    assert res[1]["error"].code == "camera_limit"
    assert len(server.calls("POST", "/cameras/bulk")) == 1


def test_bulk_duplicate_ids_400_is_reported_not_raised(server):  # type: ignore[no-untyped-def]
    server.script("POST", "/cameras/bulk", [Fail(400, code="invalid_request")])
    with mk(server) as c:
        res = c.cameras.bulk([{"name": "a", "external_id": "a"}, {"name": "a2", "external_id": "a"}])
    assert [r["ok"] for r in res] == [False, False]


@pytest.mark.asyncio
async def test_async_register_and_status(server):  # type: ignore[no-untyped-def]
    from percia import AsyncPercia

    server.script("POST", "/cameras", [Json(CREATED["body"], 201)])
    server.script("GET", "/cameras/cam_push_1/status", [Json(STATUS["online"]["body"])])
    server.script("POST", "/cameras/bulk", [Json(BULK["created"]["body"], 201)])
    server.script("GET", "/cameras/cam_push_1/status", [Fail(404, code="not_found")])
    server.script("GET", "/cameras", [Json([EXISTING["body"]["camera"]])])
    async with AsyncPercia(api_key=KEY, base_url="http://mock.test", transport=server.transport()) as c:
        reg = await c.cameras.register_push("Hall camera", "lan-cam-1")
        assert reg.token == TOKEN
        assert (await c.cameras.status("cam_push_1")).state == "online"
        res = await c.cameras.bulk(BULK_ITEMS)
        assert [r["ok"] for r in res] == [True, True]
        fallback = await c.cameras.status("cam_push_1")
        assert fallback.derived and fallback.state == "online"


def test_publish_commands_never_contain_the_token():
    cmds = build_publish_commands(WHIP, "rtsp://u:p@192.168.1.20/s", api_base="https://percia.test/api")
    assert "pc_" not in json.dumps(cmds)
    assert (
        cmds["ffmpeg"]
        == f'ffmpeg -rtsp_transport tcp -i rtsp://u:p@192.168.1.20/s -an -c:v copy -f whip -authorization "{TOKEN_PLACEHOLDER}" {WHIP}'
    )
    assert cmds["heartbeat"].endswith("https://percia.test/api/cam/heartbeat")
    assert "whipclientsink" in cmds["gstreamer"] and cmds["obs"]["service"] == "WHIP"
    assert "libx264" in build_publish_commands(WHIP, "rtsp://h/s", mode="transcode")["ffmpeg"]


def test_argv_and_scrub():
    assert publish_argv(WHIP, TOKEN, "rtsp://h/s") == [
        "-rtsp_transport",
        "tcp",
        "-i",
        "rtsp://h/s",
        "-an",
        "-c:v",
        "copy",
        "-f",
        "whip",
        "-authorization",
        TOKEN,
        WHIP,
    ]
    assert scrub_token(f"x {TOKEN} y {TOKEN}", TOKEN) == "x [token] y [token]"
    assert scrub_token("x", None) == "x"
