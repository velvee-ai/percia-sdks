"""Percia Python SDK.

>>> from percia import Percia
>>> client = Percia(api_key="pk_live_...")
"""

from __future__ import annotations

from ._billing import Billing, billing_of, describe_billing
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
from ._push import (
    TOKEN_ENV,
    TOKEN_PLACEHOLDER,
    CameraStatus,
    PushRegistration,
    build_publish_commands,
    publish_argv,
    scrub_token,
)
from ._retry import RetryPolicy
from ._stream import End, Event, Open, Ping, Reconnect, Resync, StreamItem
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
    "Billing",
    "AuthenticationError",
    "ConflictError",
    "ConnectionError",
    "DEFAULT_BASE_URL",
    "End",
    "Event",
    "Open",
    "Ping",
    "Reconnect",
    "Resync",
    "StreamItem",
    "TOKEN_ENV",
    "TOKEN_PLACEHOLDER",
    "InsufficientScopeError",
    "NotFoundError",
    "Percia",
    "PerciaError",
    "PermissionDeniedError",
    "RateLimitError",
    "CameraStatus",
    "PushRegistration",
    "RetryPolicy",
    "ServerError",
    "ValidationError",
    "WebhookSignatureError",
    "__version__",
    "billing_of",
    "build_publish_commands",
    "check_webhook_signature",
    "describe_billing",
    "publish_argv",
    "scrub_token",
    "verify_and_parse",
    "verify_webhook_signature",
]
