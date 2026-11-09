"""Verify a Percia webhook. Standard library only. Contract: docs/integrators/webhooks.md.

Header: ``Percia-Signature: t=<unix seconds>,v1=<hex HMAC-SHA256(secret, "<t>.<raw body>")>``
The SDK has the same function: ``from percia import verify_webhook_signature``.
"""

from __future__ import annotations

import hashlib
import hmac
import time
from typing import Optional

TOLERANCE_S = 300


class SignatureError(Exception):
    """``code`` is one of ``malformed``, ``stale_timestamp``, ``mismatch``."""

    def __init__(self, code: str) -> None:
        super().__init__(code)
        self.code = code


def verify(secret: str, header: Optional[str], raw_body: bytes, now: Optional[float] = None) -> None:
    timestamp: Optional[int] = None
    candidates = []
    for part in (header or "").split(","):
        key, sep, value = part.strip().partition("=")
        if not sep:
            continue
        if key == "t" and value.isascii() and value.isdigit() and len(value) <= 12:
            timestamp = int(value)
        elif key == "v1" and value:
            candidates.append(value)
    if timestamp is None or not candidates:
        raise SignatureError("malformed")
    if abs((time.time() if now is None else now) - timestamp) > TOLERANCE_S:
        raise SignatureError("stale_timestamp")
    expected = hmac.new(secret.encode(), f"{timestamp}.".encode() + raw_body, hashlib.sha256).hexdigest()
    if not any(hmac.compare_digest(expected, c) for c in candidates):
        raise SignatureError("mismatch")
