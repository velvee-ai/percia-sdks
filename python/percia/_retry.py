"""Retry policy and httpx transports that apply it (sync and async).

429 is retried for every method (the request was refused before it ran). 5xx and read timeouts are retried only for
idempotent methods (GET, HEAD, PUT, DELETE, OPTIONS) unless ``retry_non_idempotent`` is set, because a create that
answered 5xx may or may not have created the resource (docs/integrators/errors.md). Connect errors (nothing was sent)
are retried for every method.
"""

from __future__ import annotations

import asyncio
import random
import time
from dataclasses import dataclass
from typing import Callable, Optional

import httpx

from ._errors import parse_retry_after

IDEMPOTENT_METHODS = frozenset({"GET", "HEAD", "PUT", "DELETE", "OPTIONS"})
RETRYABLE_5XX = frozenset({500, 502, 503, 504})

# Indirection so tests can patch the sleeps without slowing down or touching the global time module.
_sleep: Callable[[float], None] = time.sleep


async def _asleep(seconds: float) -> None:
    await asyncio.sleep(seconds)


@dataclass
class RetryPolicy:
    max_retries: int = 2
    backoff_base: float = 0.5
    backoff_max: float = 30.0
    #: Longest Retry-After we are willing to sleep for (longer values are clamped, not skipped).
    max_retry_after: float = 60.0
    retry_non_idempotent: bool = False
    jitter: Callable[[], float] = random.random

    def should_retry_status(self, method: str, status: int) -> bool:
        if status == 429:
            return True
        if status in RETRYABLE_5XX:
            return self.retry_non_idempotent or method.upper() in IDEMPOTENT_METHODS
        return False

    def should_retry_exception(self, method: str, exc: Exception) -> bool:
        if isinstance(exc, (httpx.ConnectError, httpx.ConnectTimeout)):
            return True
        if isinstance(exc, (httpx.ReadTimeout, httpx.ReadError, httpx.RemoteProtocolError, httpx.WriteError)):
            return self.retry_non_idempotent or method.upper() in IDEMPOTENT_METHODS
        return False

    def delay(self, attempt: int, response: Optional[httpx.Response] = None) -> float:
        """Seconds to sleep before retry number ``attempt`` (0-based). Retry-After wins over backoff."""
        if response is not None:
            ra = parse_retry_after(response.headers.get("retry-after"))
            if ra is not None:
                return min(ra, self.max_retry_after)
        ceiling = min(self.backoff_max, self.backoff_base * (2**attempt))
        return float(ceiling * (0.5 + 0.5 * self.jitter()))  # "equal jitter": between half and the full ceiling


class RetryTransport(httpx.BaseTransport):
    def __init__(self, inner: httpx.BaseTransport, policy: RetryPolicy) -> None:
        self._inner = inner
        self._policy = policy

    def handle_request(self, request: httpx.Request) -> httpx.Response:
        attempt = 0
        while True:
            try:
                response = self._inner.handle_request(request)
            except httpx.TransportError as exc:
                if attempt >= self._policy.max_retries or not self._policy.should_retry_exception(request.method, exc):
                    raise
                _sleep(self._policy.delay(attempt))
                attempt += 1
                continue
            if attempt < self._policy.max_retries and self._policy.should_retry_status(
                request.method, response.status_code
            ):
                delay = self._policy.delay(attempt, response)
                response.read()
                response.close()
                _sleep(delay)
                attempt += 1
                continue
            return response

    def close(self) -> None:
        self._inner.close()


class AsyncRetryTransport(httpx.AsyncBaseTransport):
    def __init__(self, inner: httpx.AsyncBaseTransport, policy: RetryPolicy) -> None:
        self._inner = inner
        self._policy = policy

    async def handle_async_request(self, request: httpx.Request) -> httpx.Response:
        attempt = 0
        while True:
            try:
                response = await self._inner.handle_async_request(request)
            except httpx.TransportError as exc:
                if attempt >= self._policy.max_retries or not self._policy.should_retry_exception(request.method, exc):
                    raise
                await _asleep(self._policy.delay(attempt))
                attempt += 1
                continue
            if attempt < self._policy.max_retries and self._policy.should_retry_status(
                request.method, response.status_code
            ):
                delay = self._policy.delay(attempt, response)
                await response.aread()
                await response.aclose()
                await _asleep(delay)
                attempt += 1
                continue
            return response

    async def aclose(self) -> None:
        await self._inner.aclose()
