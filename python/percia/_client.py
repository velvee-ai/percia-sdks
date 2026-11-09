"""The two clients. They share one design: a configured httpx client (bearer auth + retry transport) is handed to
the generated client, so every call, generated or raw, gets the same auth, retries and error mapping."""

from __future__ import annotations

from typing import Any, AsyncIterator, Dict, Iterator, Mapping, Optional, Union

import httpx

from ._config import default_headers, normalize_base_url, resolve_credentials
from ._errors import ConnectionError, error_from_response
from ._generated.client import AuthenticatedClient
from ._generated.models.event import Event
from ._generated.models.watch import Watch
from ._retry import AsyncRetryTransport, RetryPolicy, RetryTransport

Timeout = Union[float, httpx.Timeout, None]


def _make_policy(max_retries: int, retry_non_idempotent: bool, policy: Optional[RetryPolicy]) -> RetryPolicy:
    if policy is not None:
        return policy
    if max_retries < 0:
        raise ValueError("max_retries must be >= 0")
    return RetryPolicy(max_retries=max_retries, retry_non_idempotent=retry_non_idempotent)


def _ok(status: int) -> bool:
    return 200 <= status < 300


def _parse_json(resp: httpx.Response) -> Any:
    return resp.json() if resp.content else None


class Percia:
    """Synchronous client.

    >>> client = Percia(api_key="pk_live_...")              # or oauth_token=..., or PERCIA_API_KEY in the environment
    >>> client.watches.list()
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        *,
        oauth_token: Optional[str] = None,
        base_url: Optional[str] = None,
        max_retries: int = 2,
        timeout: Timeout = 30.0,
        retry_non_idempotent: bool = False,
        retry_policy: Optional[RetryPolicy] = None,
        transport: Optional[httpx.BaseTransport] = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> None:
        from ._resources import Account, Cameras, Events, Hooks, Integrations, Watches

        token = resolve_credentials(api_key, oauth_token)
        self.base_url = normalize_base_url(base_url)
        self.retry_policy = _make_policy(max_retries, retry_non_idempotent, retry_policy)
        self._http = httpx.Client(
            base_url=self.base_url,
            headers=default_headers(token, headers),
            timeout=timeout,
            transport=RetryTransport(transport or httpx.HTTPTransport(), self.retry_policy),
        )
        self._gen = AuthenticatedClient(base_url=self.base_url, token=token)
        self._gen.set_httpx_client(self._http)
        self.watches = Watches(self)
        self.events = Events(self)
        self.cameras = Cameras(self)
        self.integrations = Integrations(self)
        self.hooks = Hooks(self)
        self.account = Account(self)

    # -- plumbing ---------------------------------------------------------------------------------------------

    def _send(self, **kwargs: Any) -> httpx.Response:
        try:
            return self._http.request(**kwargs)
        except httpx.TransportError as exc:
            raise ConnectionError(f"{type(exc).__name__}: {exc}") from exc

    def _call(self, module: Any, **kwargs: Any) -> Any:
        """Run one generated operation: build the request with its ``_get_kwargs``, send it through the retrying
        transport, raise a typed error on non-2xx, else return what the generated ``_parse_response`` makes of it."""
        resp = self._send(**module._get_kwargs(**kwargs))
        if not _ok(resp.status_code):
            raise error_from_response(resp.status_code, resp.content, resp.headers)
        return module._parse_response(client=self._gen, response=resp)

    def request(
        self,
        method: str,
        path: str,
        *,
        json: Any = None,
        params: Optional[Mapping[str, Any]] = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """Escape hatch: call any route (``path`` relative to ``/api``, e.g. ``"/watches/mine"``). Returns parsed JSON."""
        kw: Dict[str, Any] = {"method": method.upper(), "url": "/" + path.lstrip("/")}
        if json is not None:
            kw["json"] = json
        if params:
            kw["params"] = {k: v for k, v in params.items() if v is not None}
        if headers:
            kw["headers"] = dict(headers)
        resp = self._send(**kw)
        if not _ok(resp.status_code):
            raise error_from_response(resp.status_code, resp.content, resp.headers)
        return _parse_json(resp)

    # -- pagination -------------------------------------------------------------------------------------------

    def iter_events(
        self,
        *,
        watch_id: Optional[str] = None,
        type: Optional[str] = None,  # noqa: A002
        since: Union[None, str, int, float, Any] = None,
        limit: int = 50,
    ) -> Iterator[Event]:
        """Every event of every watch, newest first, following ``nextCursor`` until it is null."""
        cursor: Optional[str] = None
        seen = set()
        while True:
            page = self.events.list(limit=limit, cursor=cursor, watch_id=watch_id, type=type, since=since)
            yield from page.events
            cursor = page.next_cursor
            if not cursor or cursor in seen:
                return
            seen.add(cursor)

    def iter_watch_events(self, watch_id: str, *, limit: int = 50) -> Iterator[Event]:
        """Every event of one watch, newest first."""
        cursor: Optional[str] = None
        seen = set()
        while True:
            page = self.watches.events(watch_id, limit=limit, cursor=cursor)
            yield from page.events
            cursor = page.next_cursor
            if not cursor or cursor in seen:
                return
            seen.add(cursor)

    def iter_watches(self) -> Iterator[Watch]:
        """The watch list is not paginated by the API; this is ``watches.list()`` as an iterator for symmetry."""
        yield from self.watches.list()

    # -- lifecycle --------------------------------------------------------------------------------------------

    def close(self) -> None:
        self._http.close()

    def __enter__(self) -> Percia:
        return self

    def __exit__(self, *exc: Any) -> None:
        self.close()


class AsyncPercia:
    """Asynchronous client with the same surface as :class:`Percia`; every call is awaitable and the iterators are
    async generators (``async for event in client.iter_events(): ...``)."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        *,
        oauth_token: Optional[str] = None,
        base_url: Optional[str] = None,
        max_retries: int = 2,
        timeout: Timeout = 30.0,
        retry_non_idempotent: bool = False,
        retry_policy: Optional[RetryPolicy] = None,
        transport: Optional[httpx.AsyncBaseTransport] = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> None:
        from ._aresources import AsyncAccount, AsyncCameras, AsyncEvents, AsyncHooks, AsyncIntegrations, AsyncWatches

        token = resolve_credentials(api_key, oauth_token)
        self.base_url = normalize_base_url(base_url)
        self.retry_policy = _make_policy(max_retries, retry_non_idempotent, retry_policy)
        self._http = httpx.AsyncClient(
            base_url=self.base_url,
            headers=default_headers(token, headers),
            timeout=timeout,
            transport=AsyncRetryTransport(transport or httpx.AsyncHTTPTransport(), self.retry_policy),
        )
        self._gen = AuthenticatedClient(base_url=self.base_url, token=token)
        self._gen.set_async_httpx_client(self._http)
        self.watches = AsyncWatches(self)
        self.events = AsyncEvents(self)
        self.cameras = AsyncCameras(self)
        self.integrations = AsyncIntegrations(self)
        self.hooks = AsyncHooks(self)
        self.account = AsyncAccount(self)

    async def _send(self, **kwargs: Any) -> httpx.Response:
        try:
            return await self._http.request(**kwargs)
        except httpx.TransportError as exc:
            raise ConnectionError(f"{type(exc).__name__}: {exc}") from exc

    async def _call(self, module: Any, **kwargs: Any) -> Any:
        resp = await self._send(**module._get_kwargs(**kwargs))
        if not _ok(resp.status_code):
            raise error_from_response(resp.status_code, resp.content, resp.headers)
        return module._parse_response(client=self._gen, response=resp)

    async def request(
        self,
        method: str,
        path: str,
        *,
        json: Any = None,
        params: Optional[Mapping[str, Any]] = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        kw: Dict[str, Any] = {"method": method.upper(), "url": "/" + path.lstrip("/")}
        if json is not None:
            kw["json"] = json
        if params:
            kw["params"] = {k: v for k, v in params.items() if v is not None}
        if headers:
            kw["headers"] = dict(headers)
        resp = await self._send(**kw)
        if not _ok(resp.status_code):
            raise error_from_response(resp.status_code, resp.content, resp.headers)
        return _parse_json(resp)

    async def iter_events(
        self,
        *,
        watch_id: Optional[str] = None,
        type: Optional[str] = None,  # noqa: A002
        since: Union[None, str, int, float, Any] = None,
        limit: int = 50,
    ) -> AsyncIterator[Event]:
        cursor: Optional[str] = None
        seen = set()
        while True:
            page = await self.events.list(limit=limit, cursor=cursor, watch_id=watch_id, type=type, since=since)
            for ev in page.events:
                yield ev
            cursor = page.next_cursor
            if not cursor or cursor in seen:
                return
            seen.add(cursor)

    async def iter_watch_events(self, watch_id: str, *, limit: int = 50) -> AsyncIterator[Event]:
        cursor: Optional[str] = None
        seen = set()
        while True:
            page = await self.watches.events(watch_id, limit=limit, cursor=cursor)
            for ev in page.events:
                yield ev
            cursor = page.next_cursor
            if not cursor or cursor in seen:
                return
            seen.add(cursor)

    async def iter_watches(self) -> AsyncIterator[Watch]:
        for w in await self.watches.list():
            yield w

    async def aclose(self) -> None:
        await self._http.aclose()

    async def __aenter__(self) -> AsyncPercia:
        return self

    async def __aexit__(self, *exc: Any) -> None:
        await self.aclose()
