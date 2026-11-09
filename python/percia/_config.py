from __future__ import annotations

import datetime as _dt
import os
from typing import Any, Dict, Mapping, Optional, Type, TypeVar, Union

DEFAULT_BASE_URL = "https://playground.percia.ai"
ENV_API_KEY = "PERCIA_API_KEY"
ENV_BASE_URL = "PERCIA_BASE_URL"

T = TypeVar("T")


def normalize_base_url(base_url: Optional[str]) -> str:
    """Accept a host (``https://host``) or the API root (``https://host/api``); always return ``.../api``."""
    url = (base_url or os.environ.get(ENV_BASE_URL) or DEFAULT_BASE_URL).strip().rstrip("/")
    return url if url.endswith("/api") else url + "/api"


def resolve_credentials(api_key: Optional[str], oauth_token: Optional[str]) -> str:
    if api_key and oauth_token:
        raise ValueError("pass either api_key or oauth_token, not both")
    token = api_key or oauth_token or os.environ.get(ENV_API_KEY)
    if not token:
        raise ValueError(f"no credential: pass api_key=..., oauth_token=..., or set {ENV_API_KEY}")
    return token


def default_headers(token: str, extra: Optional[Mapping[str, str]] = None) -> Dict[str, str]:
    from ._version import __version__

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
        "User-Agent": f"percia-python/{__version__}",
    }
    headers.update(extra or {})
    return headers


def coerce_body(cls: Type[T], value: Union[T, Mapping[str, Any]]) -> T:
    """Accept either the generated body model or a plain dict in the API's JSON shape (camelCase keys)."""
    if isinstance(value, cls):
        return value
    return cls.from_dict(dict(value))  # type: ignore[attr-defined, no-any-return, arg-type]


def time_param(value: Union[None, str, int, float, _dt.datetime]) -> Optional[str]:
    """``since`` accepts ISO 8601 text, unix seconds, or a datetime."""
    if value is None:
        return None
    if isinstance(value, _dt.datetime):
        return value.isoformat()
    return str(int(value)) if isinstance(value, float) and value.is_integer() else str(value)
