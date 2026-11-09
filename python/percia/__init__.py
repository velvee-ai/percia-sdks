"""Percia Python SDK.

>>> from percia import Percia
>>> client = Percia(api_key="pk_live_...")
"""

from __future__ import annotations

from ._client import AsyncPercia, Percia
from ._config import DEFAULT_BASE_URL
from ._errors import (
    APIError,
    AuthenticationError,
    ConflictError,
    ConnectionError,
    InsufficientScopeError,
    NotFoundError,
    PerciaError,
    PermissionDeniedError,
    RateLimitError,
    ServerError,
    ValidationError,
)
from ._retry import RetryPolicy
from ._version import __version__
from ._webhooks import (
    WebhookSignatureError,
    check_webhook_signature,
    verify_and_parse,
    verify_webhook_signature,
)

__all__ = [
    "APIError",
    "AsyncPercia",
    "AuthenticationError",
    "ConflictError",
    "ConnectionError",
    "DEFAULT_BASE_URL",
    "InsufficientScopeError",
    "NotFoundError",
    "Percia",
    "PerciaError",
    "PermissionDeniedError",
    "RateLimitError",
    "RetryPolicy",
    "ServerError",
    "ValidationError",
    "WebhookSignatureError",
    "__version__",
    "check_webhook_signature",
    "verify_and_parse",
    "verify_webhook_signature",
]
