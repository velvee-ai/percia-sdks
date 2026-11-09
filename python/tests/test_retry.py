from __future__ import annotations

import httpx
import pytest

from percia import ConnectionError, Percia, RateLimitError, RetryPolicy, ServerError
from percia._retry import RetryPolicy as Policy

from .conftest import KEY
from .mock_server import Fail, Json, MockPercia

OK_CAMERA = Json(
    {
        "camera": {"id": "cam_1", "name": "Hall", "status": "never", "lastSeenAt": None, "watchCount": 0},
        "pairUrl": "https://p/cam/t",
        "pairExpiresAt": "2026-11-09T10:10:00Z",
    },
    201,
)


def mk(server: MockPercia, **kw):  # type: ignore[no-untyped-def]
    return Percia(api_key=KEY, base_url="http://mock.test", transport=server.transport(), **kw)


def test_429_honors_retry_after_seconds(server, sleeps):  # type: ignore[no-untyped-def]
    server.script("GET", "/watches/mine", [Fail(429, code="rate_limited", retry_after="3")])
    with mk(server) as c:
        assert c.watches.list()
    assert sleeps == [3.0]
    assert len(server.calls("GET", "/watches/mine")) == 2


def test_429_retry_after_http_date(server, sleeps):  # type: ignore[no-untyped-def]
    import time
    from email.utils import formatdate

    server.script("GET", "/watches/mine", [Fail(429, retry_after=formatdate(time.time() + 20, usegmt=True))])
    with mk(server) as c:
        c.watches.list()
    assert len(sleeps) == 1 and 15 <= sleeps[0] <= 20


def test_retry_after_is_clamped(server, sleeps):  # type: ignore[no-untyped-def]
    server.script("GET", "/watches/mine", [Fail(429, retry_after="3600")])
    with mk(server) as c:
        c.watches.list()
    assert sleeps == [60.0]


def test_429_is_retried_for_post(server, sleeps):  # type: ignore[no-untyped-def]
    server.script("POST", "/cameras", [Fail(429, retry_after="1"), OK_CAMERA])
    with mk(server) as c:
        res = c.cameras.create("Hall")
    assert res.pair_url == "https://p/cam/t"
    assert len(server.calls("POST", "/cameras")) == 2 and sleeps == [1.0]


def test_5xx_get_retried_with_exponential_backoff(server, sleeps):  # type: ignore[no-untyped-def]
    server.script("GET", "/watches/mine", [Fail(503), Fail(502), Json([])])
    with mk(server, max_retries=3) as c:
        assert c.watches.list() == []
    assert len(sleeps) == 2
    assert 0.25 <= sleeps[0] <= 0.5 and 0.5 <= sleeps[1] <= 1.0  # base 0.5 * 2**n, equal jitter


def test_backoff_is_capped():
    p = RetryPolicy(backoff_base=1, backoff_max=5, jitter=lambda: 1.0)
    assert [p.delay(i) for i in range(5)] == [1, 2, 4, 5, 5]
    assert Policy(backoff_base=1, jitter=lambda: 0.0).delay(0) == 0.5


def test_5xx_post_is_not_retried_by_default(server, sleeps):  # type: ignore[no-untyped-def]
    server.script("POST", "/cameras", [Fail(503), OK_CAMERA])
    with mk(server) as c, pytest.raises(ServerError):
        c.cameras.create("Hall")
    assert len(server.calls("POST", "/cameras")) == 1 and sleeps == []


def test_5xx_post_retried_when_opted_in(server, sleeps):  # type: ignore[no-untyped-def]
    server.script("POST", "/cameras", [Fail(503), OK_CAMERA])
    with mk(server, retry_non_idempotent=True) as c:
        assert c.cameras.create("Hall").camera.id == "cam_1"
    assert len(server.calls("POST", "/cameras")) == 2


def test_delete_is_idempotent_so_5xx_is_retried(server, sleeps):  # type: ignore[no-untyped-def]
    server.script("DELETE", "/hooks/hk_1", [Fail(500), Json({"ok": True, "deleted": True})])
    with mk(server) as c:
        assert c.hooks.delete("hk_1").deleted is True


@pytest.mark.parametrize("status", [400, 401, 403, 404, 409, 422])
def test_4xx_is_never_retried(server, sleeps, status):  # type: ignore[no-untyped-def]
    server.script("GET", "/watches/mine", [Fail(status)] * 3)
    with mk(server) as c, pytest.raises(Exception):  # noqa: B017
        c.watches.list()
    assert len(server.calls("GET", "/watches/mine")) == 1 and sleeps == []


def test_gives_up_after_max_retries(server, sleeps):  # type: ignore[no-untyped-def]
    server.script("GET", "/watches/mine", [Fail(429, retry_after="1")] * 10)
    with mk(server, max_retries=2) as c, pytest.raises(RateLimitError):
        c.watches.list()
    assert len(server.calls("GET", "/watches/mine")) == 3 and sleeps == [1.0, 1.0]


def test_max_retries_zero_disables_retries(server, sleeps):  # type: ignore[no-untyped-def]
    server.script("GET", "/watches/mine", [Fail(503)] * 3)
    with mk(server, max_retries=0) as c, pytest.raises(ServerError):
        c.watches.list()
    assert len(server.calls("GET", "/watches/mine")) == 1


def test_negative_max_retries_rejected(server):  # type: ignore[no-untyped-def]
    with pytest.raises(ValueError):
        mk(server, max_retries=-1)


def test_connect_error_is_retried_for_any_method(server, sleeps):  # type: ignore[no-untyped-def]
    server.script("POST", "/cameras", [httpx.ConnectError("refused"), OK_CAMERA])
    with mk(server) as c:
        assert c.cameras.create("Hall").camera.id == "cam_1"
    assert len(sleeps) == 1


def test_connect_error_exhausted_raises_percia_connection_error(server, sleeps):  # type: ignore[no-untyped-def]
    server.script("GET", "/watches/mine", [httpx.ConnectError("refused")] * 5)
    with mk(server, max_retries=2) as c, pytest.raises(ConnectionError) as exc:
        c.watches.list()
    assert isinstance(exc.value.__cause__, httpx.ConnectError) and len(sleeps) == 2


def test_read_timeout_not_retried_for_post(server, sleeps):  # type: ignore[no-untyped-def]
    server.script("POST", "/cameras", [httpx.ReadTimeout("slow"), OK_CAMERA])
    with mk(server) as c, pytest.raises(ConnectionError):
        c.cameras.create("Hall")
    assert sleeps == []


def test_read_timeout_retried_for_get(server, sleeps):  # type: ignore[no-untyped-def]
    server.script("GET", "/watches/mine", [httpx.ReadTimeout("slow"), Json([])])
    with mk(server) as c:
        assert c.watches.list() == []


def test_custom_policy_wins(server, sleeps):  # type: ignore[no-untyped-def]
    server.script("GET", "/watches/mine", [Fail(503), Fail(503), Json([])])
    pol = RetryPolicy(max_retries=2, backoff_base=10, backoff_max=10, jitter=lambda: 1.0)
    with mk(server, retry_policy=pol) as c:
        c.watches.list()
    assert sleeps == [10.0, 10.0]
