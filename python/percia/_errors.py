"""Typed errors. Branch on the exception class or on `.code`, never on the message text."""

from __future__ import annotations

import json
import re
from typing import Any, Mapping, Optional

REQUEST_ID_HEADER = "x-percia-request-id"


class PerciaError(Exception):
    """Base class of everything this SDK raises on purpose."""


class ConnectionError(PerciaError):  # noqa: A001 - mirrors the HTTP client's wording; import it from percia, not builtins
    """The request never got an HTTP answer (DNS, connect, TLS, timeout), after the configured retries."""


class APIError(PerciaError):
    """The API answered with a non-2xx status.

    Attributes:
        status: HTTP status.
        code: stable machine-readable code from ``error.code`` (e.g. ``insufficient_scope``), or None.
        message: human text. Do not branch on it.
        field: the offending request field on validation errors.
        request_id: quote this when reporting a problem (``x-percia-request-id``).
        body: the parsed JSON body, if any.
    """

    def __init__(
        self,
        status: int,
        message: str,
        *,
        code: Optional[str] = None,
        field: Optional[str] = None,
        request_id: Optional[str] = None,
        body: Any = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> None:
        super().__init__(
            f"{status} {code or 'error'}: {message}" + (f" (request_id {request_id})" if request_id else "")
        )
        self.status = status
        self.code = code
        self.message = message
        self.field = field
        self.request_id = request_id
        self.body = body
        self.headers = dict(headers or {})


class ValidationError(APIError):
    """400/422: a field failed validation. ``field`` names the first invalid one."""


class AuthenticationError(APIError):
    """401: missing, invalid or expired credential."""


class PermissionDeniedError(APIError):
    """403: the credential is valid but not allowed. (Named to avoid shadowing the builtin PermissionError.)"""


class InsufficientScopeError(PermissionDeniedError):
    """403 ``insufficient_scope``. ``required_scope`` is the scope the message names, e.g. ``hooks:write``."""

    required_scope: Optional[str]


class NotFoundError(APIError):
    """404: no such resource, or it is not yours."""


class ConflictError(APIError):
    """409: e.g. ``camera_in_use``, ``agent_in_use``, ``nothing_to_publish``."""


class RateLimitError(APIError):
    """429. ``retry_after`` is seconds from the Retry-After header when present. ``code`` ``plan_limit`` is a quota, not a rate."""

    retry_after: Optional[float]


class ServerError(APIError):
    """5xx."""


_SCOPE_RE = re.compile(r"\b([a-z]+:(?:read|write|delete))\b")


def parse_retry_after(value: Optional[str], now: Optional[float] = None) -> Optional[float]:
    """Seconds to wait from a Retry-After header: delta-seconds or an HTTP date. None when absent or unparsable."""
    if not value:
        return None
    value = value.strip()
    try:
        secs = float(value)
    except ValueError:
        import time
        from email.utils import parsedate_to_datetime

        try:
            when = parsedate_to_datetime(value)
        except (TypeError, ValueError):
            return None
        return max(0.0, when.timestamp() - (time.time() if now is None else now))
    return secs if secs >= 0 else None


def error_from_response(status: int, content: bytes, headers: Mapping[str, str]) -> APIError:
    """Build the right APIError subclass from a status, raw body and headers (a mapping with case-insensitive get)."""
    body: Any = None
    try:
        body = json.loads(content) if content else None
    except ValueError:
        body = None
    err: Mapping[str, Any] = {}
    if isinstance(body, dict):
        inner = body.get("error")
        err = inner if isinstance(inner, dict) else {}
    code = err.get("code") if isinstance(err.get("code"), str) else None
    message = err.get("message") if isinstance(err.get("message"), str) else None
    if message is None and isinstance(body, dict) and isinstance(body.get("message"), str):
        message = body["message"]
    if message is None:
        message = content.decode("utf-8", "replace")[:200] if content else f"HTTP {status}"
    field = err.get("field") if isinstance(err.get("field"), str) else None
    request_id = (
        err.get("request_id")
        if isinstance(err.get("request_id"), str)
        else body.get("request_id")
        if isinstance(body, dict) and isinstance(body.get("request_id"), str)
        else headers.get(REQUEST_ID_HEADER)
    )
    kw: dict[str, Any] = dict(code=code, field=field, request_id=request_id, body=body, headers=headers)
    if status == 401:
        return AuthenticationError(status, message, **kw)
    if status == 403:
        if code == "insufficient_scope":
            e = InsufficientScopeError(status, message, **kw)
            m = _SCOPE_RE.search(message)
            e.required_scope = m.group(1) if m else None
            return e
        return PermissionDeniedError(status, message, **kw)
    if status == 404:
        return NotFoundError(status, message, **kw)
    if status == 409:
        return ConflictError(status, message, **kw)
    if status == 429:
        e2 = RateLimitError(status, message, **kw)
        e2.retry_after = parse_retry_after(headers.get("retry-after"))
        return e2
    if status in (400, 422):
        return ValidationError(status, message, **kw)
    if status >= 500:
        return ServerError(status, message, **kw)
    return APIError(status, message, **kw)
