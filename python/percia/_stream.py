"""Developer event feed: ``GET /api/events/stream`` (Server-Sent Events), for local development and tests.

``client.events.stream(...)`` is an iterator (``async for`` on :class:`AsyncPercia`) that reconnects with the last cursor,
honours ``Retry-After``, dedupes on ``eventId`` and yields :class:`Open`, :class:`Event`, :class:`Resync`, :class:`End`,
:class:`Reconnect` and :class:`Ping` items. It is not a delivery path: webhooks stay the production path. Contract:
percia-cf ``docs/specs/platform/dev-feed.md``.

Stop it by leaving the loop (``break``) or by calling ``close()`` (``aclose()`` async) on the iterator.
"""

from __future__ import annotations

import json
import random as _random
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, AsyncIterator, Callable, Dict, Iterator, List, Optional, Set, Tuple, Union

import httpx

from . import _retry
from ._errors import APIError, ConnectionError, error_from_response, parse_retry_after

if TYPE_CHECKING:
    from ._client import AsyncPercia, Percia

DEFAULT_RETRY_MS = 3000
SEEN_MAX = 2000


@dataclass
class Open:
    """The stream is live (``: connected``). ``attempt`` is 1 on the first connection."""

    attempt: int
    kind: str = "open"


@dataclass
class Event:
    """One event. ``data`` is the exact JSON string the server sent: sign and forward that string, not a re-serialisation."""

    cursor: str
    event: Dict[str, Any]
    data: str
    kind: str = "event"


@dataclass
class Resync:
    """The cursor is older than the replay window (5000 events): backfill with ``GET /api/events`` once."""

    reason: str
    from_: Optional[str] = None
    kind: str = "resync"


@dataclass
class End:
    """The server closed the stream on purpose (``max_duration`` every 10 minutes, ``lease_lost``, ``error``). The iterator reconnects by itself."""

    reason: str
    kind: str = "end"


@dataclass
class Reconnect:
    """The connection failed or ended; the iterator waits ``delay`` seconds and reconnects with the last cursor."""

    attempt: int
    delay: float
    reason: str
    status: Optional[int] = None
    code: Optional[str] = None
    message: Optional[str] = None
    kind: str = "reconnect"


@dataclass
class Ping:
    kind: str = "ping"


StreamItem = Union[Open, Event, Resync, End, Reconnect, Ping]

# (kind, ...) tuples keep the parser tiny: ("comment", text) | ("retry", ms) | ("message", id, event, data)
Frame = Tuple[Any, ...]


class SseParser:
    """Incremental SSE parser (WHATWG rules: LF, CR or CRLF line ends, multi-line ``data``, comments, ``retry``, BOM).

    Splits on CR and LF only: ``str.splitlines`` would also split on U+2028 and U+0085, which may appear inside JSON.
    """

    def __init__(self) -> None:
        self._buf = ""
        self._first = True
        self._skip_lf = False
        self._id: Optional[str] = None
        self._event = ""
        self._data: List[str] = []

    def feed(self, text: str) -> List[Frame]:
        out: List[Frame] = []
        if self._first and text:
            self._first = False
            if text.startswith("﻿"):
                text = text[1:]
        for ch in text:
            if self._skip_lf:
                self._skip_lf = False
                if ch == "\n":
                    continue
            if ch in "\r\n":
                self._skip_lf = ch == "\r"
                frame = self._line(self._buf)
                self._buf = ""
                if frame is not None:
                    out.append(frame)
            else:
                self._buf += ch
        return out

    def _line(self, line: str) -> Optional[Frame]:
        if line == "":
            frame: Optional[Frame] = (
                ("message", self._id, self._event or "message", "\n".join(self._data)) if self._data else None
            )
            self._id, self._event, self._data = None, "", []
            return frame
        if line.startswith(":"):
            return ("comment", line[1:].strip())
        name, sep, value = line.partition(":")
        if sep and value.startswith(" "):
            value = value[1:]
        if name == "id":
            if "\0" not in value:
                self._id = value
        elif name == "event":
            self._event = value
        elif name == "data":
            self._data.append(value)
        elif name == "retry" and value.isdigit():
            return ("retry", int(value))
        return None


@dataclass
class _Plan:
    """The reconnect state machine shared by the sync and async loops (no I/O in here)."""

    watch_id: Optional[str]
    concern_id: Optional[str]
    type: Optional[str]
    backlog: Optional[int]
    since: Optional[str]
    max_reconnects: Optional[int]
    base_delay: float
    max_delay: float
    dedupe: bool
    jitter: Callable[[], float]
    cursor: Optional[str] = None
    retry: float = DEFAULT_RETRY_MS / 1000
    failures: int = 0
    attempt: int = 0
    first: bool = True
    seen: Set[str] = field(default_factory=set)
    seen_order: List[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.cursor = self.since

    # -- one connection -------------------------------------------------------------------------------------

    def begin(self) -> Tuple[Dict[str, Any], Dict[str, str]]:
        self.attempt += 1
        params: Dict[str, Any] = {}
        if self.watch_id:
            params["watchId"] = self.watch_id
        if self.concern_id:
            params["concernId"] = self.concern_id
        if self.type:
            params["type"] = self.type
        headers = {"accept": "text/event-stream", "cache-control": "no-cache"}
        if self.first and self.cursor is None and self.backlog:
            params["backlog"] = self.backlog
        if self.first and self.cursor is not None:
            params["since"] = self.cursor  # a given cursor goes as ?since= on the first connection...
        if not self.first and self.cursor is not None:
            headers["last-event-id"] = self.cursor  # ...and every reconnect uses Last-Event-ID
        return params, headers

    def backoff(self) -> float:
        self.failures += 1
        return float(self.jitter() * min(self.max_delay, self.base_delay * 2 ** (self.failures - 1)))

    def too_many(self) -> bool:
        return self.max_reconnects is not None and self.failures > self.max_reconnects

    def http_error(self, resp_status: int, content: bytes, headers: Any) -> Tuple[APIError, Optional[Reconnect]]:
        """A non-2xx answer. Returns the error and, when retrying can help (429, 5xx), the Reconnect to announce."""
        err = error_from_response(resp_status, content, headers)
        if resp_status != 429 and resp_status < 500:
            return err, None  # 400, 401, 403, 404: retrying cannot help
        ra = parse_retry_after(headers.get("retry-after"))
        delay = ra if ra is not None else self.backoff()
        if ra is not None:
            self.failures += 1
        return err, Reconnect(
            self.attempt + 1,
            float(delay),
            "rate_limited" if resp_status == 429 else "server_error",
            resp_status,
            err.code,
            err.message,
        )

    def frame(self, f: Frame, state: Dict[str, Any]) -> Optional[StreamItem]:
        """Turn one SSE frame into an item (or None). ``state`` carries ``opened`` and ``ended`` for this connection."""
        kind = f[0]
        if kind == "retry":
            self.retry = min(max(f[1], 250), 60_000) / 1000
            return None
        if kind == "comment":
            if f[1] == "connected":
                state["opened"] = True
                self.failures = 0
                return Open(self.attempt)
            return Ping() if f[1] == "ping" else None
        _, mid, event, data = f
        if event in ("end", "resync"):
            try:
                body = json.loads(data)
                body = body if isinstance(body, dict) else {}
            except ValueError:
                body = {}
            if event == "end":
                state["ended"] = True
                state["reason"] = body.get("reason") or "end"
                return End(state["reason"])
            frm = body.get("from")
            return Resync(body.get("reason") or "cursor_too_old", None if frm is None else str(frm))
        try:
            ev = json.loads(data)
        except ValueError:
            return None  # not JSON: not an event of this contract
        if not isinstance(ev, dict):
            return None
        if mid is not None and mid.isdigit():
            self.cursor = mid
        eid = ev.get("eventId")
        if self.dedupe and eid:
            if eid in self.seen:
                return None
            self.seen.add(eid)
            self.seen_order.append(eid)
            if len(self.seen_order) > SEEN_MAX:
                self.seen.discard(self.seen_order.pop(0))
        return Event(mid if mid is not None else (self.cursor or ""), ev, data)

    def after(self, state: Dict[str, Any], idled: bool = False) -> Reconnect:
        """The connection ended (clean close, `end` or idle): what to announce and how long to wait."""
        reason = state.get("reason") or ("idle_timeout" if idled else "closed")
        delay = self.retry
        if not state.get("opened") and not idled:
            delay = self.backoff()
            if self.too_many():
                raise ConnectionError("The event stream closed before it opened.")
        elif state.get("ended") and reason in ("lease_lost", "error"):
            delay = max(delay, self.retry)
        return Reconnect(self.attempt + 1, float(delay), reason)

    def network_error(self, exc: Exception, idled: bool) -> Reconnect:
        if idled:
            return Reconnect(self.attempt + 1, self.retry, "idle_timeout")
        delay = self.backoff()
        if self.too_many():
            raise ConnectionError(f"Could not reach Percia: {type(exc).__name__}: {exc}") from exc
        return Reconnect(self.attempt + 1, float(delay), "network_error", message=f"{type(exc).__name__}: {exc}")


def _make_plan(
    watch_id: Optional[str],
    concern_id: Optional[str],
    type: Optional[str],  # noqa: A002
    backlog: Optional[int],
    since: Union[None, int, str],
    max_reconnects: Optional[int],
    base_delay: float,
    max_delay: float,
    dedupe: bool,
    jitter: Optional[Callable[[], float]],
) -> _Plan:
    if backlog is not None and not (isinstance(backlog, int) and 0 <= backlog <= 20):
        raise ValueError("backlog must be an integer from 0 to 20")
    if since is not None and not str(since).isdigit():
        raise ValueError("since must be a non-negative integer cursor")
    return _Plan(
        watch_id, concern_id, type, backlog, None if since is None else str(since), max_reconnects,
        base_delay, max_delay, dedupe, jitter or _random.random,
    )  # fmt: skip


def _timeout(idle: Optional[float]) -> httpx.Timeout:
    return httpx.Timeout(10.0, read=idle if idle else None)


def stream_events(
    client: Percia,
    *,
    watch_id: Optional[str] = None,
    concern_id: Optional[str] = None,
    type: Optional[str] = None,  # noqa: A002
    backlog: Optional[int] = None,
    since: Union[None, int, str] = None,
    max_reconnects: Optional[int] = None,
    base_delay: float = 0.5,
    max_delay: float = 30.0,
    idle_timeout: Optional[float] = 45.0,
    dedupe: bool = True,
    jitter: Optional[Callable[[], float]] = None,
) -> Iterator[StreamItem]:
    # Validate now (a generator would defer the error to the first `next`), then hand the plan to the loop.
    plan = _make_plan(watch_id, concern_id, type, backlog, since, max_reconnects, base_delay, max_delay, dedupe, jitter)
    return _run(client, plan, idle_timeout)


def _run(client: Percia, plan: _Plan, idle_timeout: Optional[float]) -> Iterator[StreamItem]:
    while True:
        params, headers = plan.begin()
        state: Dict[str, Any] = {}
        announce: Optional[Reconnect] = None
        idled = False
        try:
            with client._http.stream(
                "GET", "/events/stream", params=params, headers=headers, timeout=_timeout(idle_timeout)
            ) as resp:
                if not resp.is_success:
                    resp.read()
                    err, announce = plan.http_error(resp.status_code, resp.content, resp.headers)
                    if announce is None or plan.too_many():
                        raise err
                else:
                    plan.first = False
                    parser = SseParser()
                    decoder = _Decoder()
                    for chunk in resp.iter_bytes():
                        for f in parser.feed(decoder.feed(chunk)):
                            item = plan.frame(f, state)
                            if item is not None:
                                yield item
        except httpx.ReadTimeout as exc:
            idled = True
            announce = plan.network_error(exc, True)
        except httpx.TransportError as exc:
            announce = plan.network_error(exc, False)
        if announce is None:
            announce = plan.after(state, idled)
        yield announce
        _retry._sleep(announce.delay)


class _Decoder:
    """Incremental UTF-8 decoding (a multi-byte character may be split across chunks)."""

    def __init__(self) -> None:
        import codecs

        self._d = codecs.getincrementaldecoder("utf-8")(errors="replace")

    def feed(self, chunk: bytes) -> str:
        return self._d.decode(chunk)


def astream_events(
    client: AsyncPercia,
    *,
    watch_id: Optional[str] = None,
    concern_id: Optional[str] = None,
    type: Optional[str] = None,  # noqa: A002
    backlog: Optional[int] = None,
    since: Union[None, int, str] = None,
    max_reconnects: Optional[int] = None,
    base_delay: float = 0.5,
    max_delay: float = 30.0,
    idle_timeout: Optional[float] = 45.0,
    dedupe: bool = True,
    jitter: Optional[Callable[[], float]] = None,
) -> AsyncIterator[StreamItem]:
    plan = _make_plan(watch_id, concern_id, type, backlog, since, max_reconnects, base_delay, max_delay, dedupe, jitter)
    return _arun(client, plan, idle_timeout)


async def _arun(client: AsyncPercia, plan: _Plan, idle_timeout: Optional[float]) -> AsyncIterator[StreamItem]:
    while True:
        params, headers = plan.begin()
        state: Dict[str, Any] = {}
        announce: Optional[Reconnect] = None
        idled = False
        try:
            async with client._http.stream(
                "GET", "/events/stream", params=params, headers=headers, timeout=_timeout(idle_timeout)
            ) as resp:
                if not resp.is_success:
                    await resp.aread()
                    err, announce = plan.http_error(resp.status_code, resp.content, resp.headers)
                    if announce is None or plan.too_many():
                        raise err
                else:
                    plan.first = False
                    parser = SseParser()
                    decoder = _Decoder()
                    async for chunk in resp.aiter_bytes():
                        for f in parser.feed(decoder.feed(chunk)):
                            item = plan.frame(f, state)
                            if item is not None:
                                yield item
        except httpx.ReadTimeout as exc:
            idled = True
            announce = plan.network_error(exc, True)
        except httpx.TransportError as exc:
            announce = plan.network_error(exc, False)
        if announce is None:
            announce = plan.after(state, idled)
        yield announce
        await _retry._asleep(announce.delay)
