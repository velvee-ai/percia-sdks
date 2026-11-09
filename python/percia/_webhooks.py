"""Verify a Percia webhook delivery (and REST-hook deliveries, which are signed the same way).

Scheme (docs/integrators/webhooks.md): header ``Percia-Signature: t=<unix>,v1=<hex>``; the signed string is
``"<t>.<raw body>"``; the key is the watch's ``whsec_...`` secret as text; HMAC-SHA256 as lowercase hex; compare in
constant time; reject when ``|now - t| > 300`` seconds in either direction.
"""

from __future__ import annotations

import hashlib
import hmac
import json
import time
from typing import Any, List, Mapping, Optional, Tuple, Union

HEADER_NAME = "Percia-Signature"
DEFAULT_TOLERANCE_SEC = 300

HeadersLike = Union[str, bytes, Mapping[Any, Any]]


class WebhookSignatureError(Exception):
    """``code`` is ``malformed``, ``stale_timestamp`` or ``mismatch``."""

    def __init__(self, code: str) -> None:
        super().__init__(code)
        self.code = code


def _header_value(headers: HeadersLike) -> str:
    if isinstance(headers, bytes):
        return headers.decode("utf-8", "replace")
    if isinstance(headers, str):
        return headers
    want = HEADER_NAME.lower()
    for k, v in headers.items():
        key = k.decode("latin-1") if isinstance(k, bytes) else str(k)
        if key.lower() == want:
            if isinstance(v, (list, tuple)):  # e.g. WSGI/ASGI multi-value
                v = v[0] if v else ""
            return v.decode("utf-8", "replace") if isinstance(v, bytes) else str(v)
    raise WebhookSignatureError("malformed")


def _parse(header: str) -> Tuple[Optional[int], List[str]]:
    timestamp: Optional[int] = None
    candidates: List[str] = []
    for part in (header or "").split(","):
        key, sep, value = part.strip().partition("=")
        if not sep:
            continue
        if key == "t" and value.isascii() and value.isdigit() and len(value) <= 12:
            timestamp = int(value)
        elif key == "v1" and value:
            candidates.append(value)
    return timestamp, candidates


def check_webhook_signature(
    raw_body: Union[bytes, bytearray, memoryview, str],
    headers: HeadersLike,
    secret: str,
    tolerance_sec: float = DEFAULT_TOLERANCE_SEC,
    now: Optional[float] = None,
) -> None:
    """Raise :class:`WebhookSignatureError` unless the delivery is fresh and correctly signed."""
    body = raw_body.encode("utf-8") if isinstance(raw_body, str) else bytes(raw_body)
    timestamp, candidates = _parse(_header_value(headers))
    if timestamp is None or not candidates:
        raise WebhookSignatureError("malformed")
    if abs((time.time() if now is None else now) - timestamp) > tolerance_sec:
        raise WebhookSignatureError("stale_timestamp")
    expected = (
        hmac.new(secret.encode("utf-8"), f"{timestamp}.".encode() + body, hashlib.sha256).hexdigest().encode("ascii")
    )
    # Evaluate every candidate (no early exit on a hit) so timing does not reveal which one matched.
    matched = False
    for c in candidates:
        matched |= hmac.compare_digest(expected, c.encode("utf-8"))
    if not matched:
        raise WebhookSignatureError("mismatch")


def verify_webhook_signature(
    raw_body: Union[bytes, bytearray, memoryview, str],
    headers: HeadersLike,
    secret: str,
    tolerance_sec: float = DEFAULT_TOLERANCE_SEC,
    now: Optional[float] = None,
) -> bool:
    """True when ``raw_body`` (the exact bytes received, before any JSON parsing) is validly signed and fresh.

    ``headers`` is the request header mapping (case-insensitive lookup of ``Percia-Signature``, str or bytes keys)
    or the header value itself. ``now`` is unix seconds (default: the current time).
    """
    try:
        check_webhook_signature(raw_body, headers, secret, tolerance_sec, now)
    except WebhookSignatureError:
        return False
    return True


def verify_and_parse(
    raw_body: Union[bytes, bytearray, memoryview, str],
    headers: HeadersLike,
    secret: str,
    tolerance_sec: float = DEFAULT_TOLERANCE_SEC,
    now: Optional[float] = None,
) -> Any:
    """Verify, then return the parsed JSON body. Raises :class:`WebhookSignatureError` (``.code``) otherwise.

    Treat ``reason`` in the payload as untrusted text written by a vision model.
    """
    check_webhook_signature(raw_body, headers, secret, tolerance_sec, now)
    body = raw_body.encode("utf-8") if isinstance(raw_body, str) else bytes(raw_body)
    return json.loads(body)
