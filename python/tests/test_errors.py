from __future__ import annotations

import httpx
import pytest

from percia import (
    APIError,
    AuthenticationError,
    ConflictError,
    InsufficientScopeError,
    NotFoundError,
    Percia,
    PerciaError,
    PermissionDeniedError,
    RateLimitError,
    ServerError,
    ValidationError,
)
from percia._errors import error_from_response, parse_retry_after

from .conftest import KEY
from .mock_server import Fail, Json, MockPercia


def mk(server: MockPercia, **kw):  # type: ignore[no-untyped-def]
    return Percia(api_key=kw.pop("api_key", KEY), base_url="http://mock.test", transport=server.transport(), **kw)


def test_authentication_error_carries_code_and_request_id(server, sleeps):  # type: ignore[no-untyped-def]
    with mk(server, api_key="pk_live_wrong") as c, pytest.raises(AuthenticationError) as exc:
        c.watches.list()
    e = exc.value
    assert (e.status, e.code) == (401, "invalid_api_key")
    assert e.request_id and e.request_id.startswith("req_mock")
    assert isinstance(e, APIError) and isinstance(e, PerciaError)
    assert "request_id" in str(e)


def test_insufficient_scope_names_the_scope(server, sleeps):  # type: ignore[no-untyped-def]
    server.keys["pk_live_ro"] = ["watches:read"]
    with mk(server, api_key="pk_live_ro") as c, pytest.raises(InsufficientScopeError) as exc:
        c.hooks.list()
    assert exc.value.required_scope == "hooks:write"
    assert isinstance(exc.value, PermissionDeniedError)
    assert exc.value.status == 403


def test_plain_403_is_permission_denied(server, sleeps):  # type: ignore[no-untyped-def]
    server.script("GET", "/watches/mine", [Fail(403, code="forbidden")])
    with mk(server) as c, pytest.raises(PermissionDeniedError) as exc:
        c.watches.list()
    assert not isinstance(exc.value, InsufficientScopeError)


def test_validation_error_exposes_field(server, sleeps):  # type: ignore[no-untyped-def]
    with mk(server) as c, pytest.raises(ValidationError) as exc:
        c.request("POST", "/hooks", json={"events": ["goal.met"]})
    assert exc.value.field == "url" and exc.value.code == "invalid_request"


def test_not_found_and_conflict(server, sleeps):  # type: ignore[no-untyped-def]
    server.script("GET", "/watches/w_missing", [Fail(404, code="not_found")])
    server.script("DELETE", "/cameras/cam_1", [Fail(409, code="camera_in_use")])
    with mk(server) as c:
        with pytest.raises(NotFoundError):
            c.watches.get("w_missing")
        with pytest.raises(ConflictError) as exc:
            c.cameras.delete("cam_1")
        assert exc.value.code == "camera_in_use"


def test_server_error_after_retries(server, sleeps):  # type: ignore[no-untyped-def]
    server.script("GET", "/watches/mine", [Fail(500)] * 5)
    with mk(server, max_retries=1) as c, pytest.raises(ServerError):
        c.watches.list()
    assert len(server.calls("GET", "/watches/mine")) == 2


def test_request_id_falls_back_to_header():
    resp = httpx.Response(400, json={"message": "bad"}, headers={"x-percia-request-id": "req_hdr"})
    e = error_from_response(resp.status_code, resp.content, resp.headers)
    assert e.request_id == "req_hdr" and e.message == "bad" and isinstance(e, ValidationError)


def test_request_id_in_top_level_body():
    e = error_from_response(500, b'{"message":"x","request_id":"req_top"}', {})
    assert e.request_id == "req_top"


def test_non_json_error_body(server, sleeps):  # type: ignore[no-untyped-def]
    server.script("GET", "/watches/mine", [Fail(502, raw=b"<html>Bad gateway</html>")] * 3)
    with mk(server) as c, pytest.raises(ServerError) as exc:
        c.watches.list()
    assert exc.value.status == 502 and "Bad gateway" in exc.value.message and exc.value.code is None


def test_rate_limit_error_has_retry_after(server, sleeps):  # type: ignore[no-untyped-def]
    server.script("GET", "/watches/mine", [Fail(429, code="rate_limited", retry_after="7")] * 2)
    with mk(server, max_retries=0) as c, pytest.raises(RateLimitError) as exc:
        c.watches.list()
    assert exc.value.retry_after == 7.0 and exc.value.code == "rate_limited"


def test_parse_retry_after_forms():
    assert parse_retry_after("5") == 5.0
    assert parse_retry_after("1.5") == 1.5
    assert parse_retry_after(None) is None and parse_retry_after("") is None and parse_retry_after("soon") is None
    assert parse_retry_after("-3") is None
    assert parse_retry_after("Wed, 21 Oct 2015 07:28:00 GMT", now=1445412480 - 10) == 10.0
    assert parse_retry_after("Wed, 21 Oct 2015 07:28:00 GMT", now=1445412480 + 10) == 0.0


def test_success_with_scripted_json(server, sleeps):  # type: ignore[no-untyped-def]
    server.script("GET", "/events", [Json({"events": [], "nextCursor": None})])
    with mk(server) as c:
        page = c.events.list()
    assert page.events == [] and page.next_cursor is None
