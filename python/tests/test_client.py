from __future__ import annotations

import pytest

from percia import AuthenticationError, Percia
from percia._config import DEFAULT_BASE_URL, normalize_base_url

from .conftest import KEY
from .mock_server import Json, MockPercia


def test_bearer_header_and_user_agent(client, server):  # type: ignore[no-untyped-def]
    client.watches.list()
    req = server.requests[-1]
    assert req.headers["authorization"] == f"Bearer {KEY}"
    assert req.headers["user-agent"].startswith("percia-python/")
    assert req.url.path == "/api/watches/mine"


def test_oauth_token_is_sent_as_bearer(server, sleeps):  # type: ignore[no-untyped-def]
    server.keys["oauth_tok"] = ["watches:read"]
    with Percia(oauth_token="oauth_tok", base_url="http://mock.test", transport=server.transport()) as c:
        c.watches.list()
    assert server.requests[-1].headers["authorization"] == "Bearer oauth_tok"


def test_credential_rules(monkeypatch):  # type: ignore[no-untyped-def]
    monkeypatch.delenv("PERCIA_API_KEY", raising=False)
    with pytest.raises(ValueError, match="no credential"):
        Percia()
    with pytest.raises(ValueError, match="not both"):
        Percia(api_key="a", oauth_token="b")
    monkeypatch.setenv("PERCIA_API_KEY", "from_env")
    c = Percia(base_url="http://x")
    assert c._http.headers["authorization"] == "Bearer from_env"
    c.close()


@pytest.mark.parametrize(
    "given, expected",
    [
        ("https://example.test", "https://example.test/api"),
        ("https://example.test/", "https://example.test/api"),
        ("https://example.test/api", "https://example.test/api"),
        ("https://example.test/api/", "https://example.test/api"),
        ("http://localhost:5173", "http://localhost:5173/api"),
    ],
)
def test_base_url_normalization(given, expected):  # type: ignore[no-untyped-def]
    assert normalize_base_url(given) == expected


def test_base_url_default_and_env(monkeypatch):  # type: ignore[no-untyped-def]
    monkeypatch.delenv("PERCIA_BASE_URL", raising=False)
    assert normalize_base_url(None) == DEFAULT_BASE_URL + "/api"
    monkeypatch.setenv("PERCIA_BASE_URL", "https://staging.test")
    assert normalize_base_url(None) == "https://staging.test/api"
    assert normalize_base_url("https://explicit.test") == "https://explicit.test/api"


def test_requests_go_to_api_prefix(client, server):  # type: ignore[no-untyped-def]
    client.request("GET", "events/sample")
    assert server.requests[-1].url.path == "/api/events/sample"


def test_raw_request_returns_parsed_json_and_drops_none_params(client, server):  # type: ignore[no-untyped-def]
    server.script("GET", "/events", [Json({"events": [], "nextCursor": None})])
    out = client.request("GET", "/events", params={"limit": 5, "cursor": None})
    assert out == {"events": [], "nextCursor": None}
    assert server.requests[-1].url.params["limit"] == "5" and "cursor" not in server.requests[-1].url.params


def test_raw_request_empty_body_is_none(client, server):  # type: ignore[no-untyped-def]
    server.script("DELETE", "/cameras/c1", [Json(None, 200)])
    server.on("DELETE", "/cameras/c2", lambda r: __import__("httpx").Response(204))
    assert client.request("DELETE", "/cameras/c2") is None


def test_raw_request_raises_typed_errors(server, sleeps):  # type: ignore[no-untyped-def]
    with Percia(api_key="pk_live_bad", base_url="http://mock.test", transport=server.transport()) as c:
        with pytest.raises(AuthenticationError):
            c.request("GET", "/watches/mine")


def test_context_manager_closes(server):  # type: ignore[no-untyped-def]
    with Percia(api_key=KEY, base_url="http://mock.test", transport=server.transport()) as c:
        pass
    assert c._http.is_closed


def test_mock_server_covers_every_operation(server):  # type: ignore[no-untyped-def]
    assert len(server._ops) >= 90 and isinstance(server, MockPercia)
