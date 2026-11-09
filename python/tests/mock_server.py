"""An offline mock of the Percia API built from spec/openapi.json.

* One handler per operation. A successful response is the spec's `example` for that operation when it has one,
  else a minimal instance generated from the response schema (every property filled, so generated parsers that
  require keys are happy).
* Auth is checked like the real API: operations whose `security` lists `bearerAuth` need ``Authorization: Bearer
  <key>`` with a key in ``keys`` that holds *all* scopes in ``x-percia-scopes``; session-only operations refuse a key.
  Errors use the shared envelope ``{"error": {code, message, request_id}, message, request_id}`` and carry
  ``x-percia-request-id``.
* Required top-level request-body properties are checked (400 ``invalid_request`` with ``field``).
* Scripted overrides: ``server.script("GET", "/events", [Fail(429, retry_after=1), ...])`` answers the next matching
  requests from the queue, then falls back to the default behaviour. ``server.on(...)`` replaces the handler.
* ``server.transport()`` is an ``httpx.MockTransport`` (works for sync and async clients); ``server.handler`` is the
  plain callable (use it with respx's ``side_effect``). ``server.requests`` logs every request.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

import httpx

SPEC_PATH = Path(__file__).resolve().parents[2] / "spec" / "openapi.json"
ALL_SCOPES = [
    "watches:read", "watches:write", "watches:delete", "events:read", "cameras:read", "cameras:write",
    "integrations:read", "integrations:write", "devices:write", "hooks:write",
]  # fmt: skip


@dataclass
class Fail:
    """A scripted failure: ``Fail(503)``, ``Fail(429, retry_after="1")``, ``Fail(500, code="internal", request_id="req_x")``."""

    status: int
    retry_after: Optional[str] = None
    code: str = "internal"
    message: str = "scripted failure"
    request_id: Optional[str] = "req_scripted"
    raw: Optional[bytes] = None  # send this body verbatim instead of the JSON envelope


@dataclass
class Json:
    """A scripted success: ``Json({"events": [], "nextCursor": None})``."""

    body: Any
    status: int = 200


Scripted = Union[Fail, Json, httpx.Response, Exception, Callable[[httpx.Request], httpx.Response]]


def _resolve(spec: Dict[str, Any], node: Any) -> Any:
    while isinstance(node, dict) and "$ref" in node:
        ref = node["$ref"]
        assert ref.startswith("#/"), ref
        cur: Any = spec
        for part in ref[2:].split("/"):
            cur = cur[part]
        node = cur
    return node


def instance(spec: Dict[str, Any], schema: Any, depth: int = 0) -> Any:
    """A minimal valid-looking value for a JSON schema (all properties filled; arrays hold one item)."""
    schema = _resolve(spec, schema)
    if schema is True or schema is False or schema is None or not isinstance(schema, dict):
        return {}
    if "const" in schema:
        return schema["const"]
    if "example" in schema:
        return schema["example"]
    if "enum" in schema:
        return next((v for v in schema["enum"] if v is not None), None)
    for key in ("oneOf", "anyOf"):
        if key in schema:
            options = [o for o in schema[key] if _resolve(spec, o).get("type") != "null"] or schema[key]
            return instance(spec, options[0], depth)
    if "allOf" in schema:
        merged: Dict[str, Any] = {}
        for part in schema["allOf"]:
            v = instance(spec, part, depth)
            if isinstance(v, dict):
                merged.update(v)
        return merged
    t = schema.get("type")
    if isinstance(t, list):
        t = next((x for x in t if x != "null"), "null")
    if t == "object" or "properties" in schema:
        if depth > 6:
            return {}
        return {k: instance(spec, v, depth + 1) for k, v in (schema.get("properties") or {}).items()}
    if t == "array":
        return [] if depth > 6 else [instance(spec, schema.get("items", {}), depth + 1)]
    if t == "string":
        fmt = schema.get("format")
        if fmt == "date-time":
            return "2026-11-09T10:00:00.000Z"
        if fmt == "date":
            return "2026-11-09"
        return "x" * max(1, schema.get("minLength", 1))
    if t == "integer":
        return int(schema.get("minimum", 0))
    if t == "number":
        return float(schema.get("minimum", 0))
    if t == "boolean":
        return False
    return None


@dataclass
class _Op:
    method: str
    template: str
    regex: re.Pattern[str]
    op: Dict[str, Any]
    operation_id: str


@dataclass
class MockPercia:
    spec: Dict[str, Any] = field(default_factory=lambda: json.loads(SPEC_PATH.read_text()))
    keys: Dict[str, List[str]] = field(default_factory=lambda: {"pk_live_test": list(ALL_SCOPES)})
    requests: List[httpx.Request] = field(default_factory=list)
    _ops: List[_Op] = field(default_factory=list)
    _scripts: List[Tuple[str, re.Pattern[str], List[Scripted]]] = field(default_factory=list)
    _custom: List[Tuple[str, re.Pattern[str], Callable[[httpx.Request], httpx.Response]]] = field(default_factory=list)
    _counter: int = 0

    def __post_init__(self) -> None:
        prefix = self.spec["servers"][0]["url"].rstrip("/")
        self.prefix = prefix
        for path, item in self.spec["paths"].items():
            # re.escape turns "{id}" into "\{id\}"; swap each escaped parameter for a path-segment matcher
            pattern = "^" + re.sub(r"\\\{[^/}]+?\\\}", "[^/]+", re.escape(prefix + path)) + "$"
            rx = re.compile(pattern)
            for method, op in item.items():
                if isinstance(op, dict) and "operationId" in op:
                    self._ops.append(_Op(method.upper(), path, rx, op, op["operationId"]))

    # -- configuration ---------------------------------------------------------------------------------------

    def script(self, method: str, path: str, responses: List[Scripted]) -> None:
        """Answer the next requests to ``method path`` (path is relative to /api, e.g. ``/events``) from this queue."""
        self._scripts.append((method.upper(), re.compile("^" + re.escape(self.prefix + path) + "$"), list(responses)))

    def on(self, method: str, path: str, fn: Callable[[httpx.Request], httpx.Response]) -> None:
        self._custom.append((method.upper(), re.compile("^" + re.escape(self.prefix + path) + "$"), fn))

    def transport(self) -> httpx.MockTransport:
        return httpx.MockTransport(self.handler)

    def calls(self, method: str, path: str) -> List[httpx.Request]:
        return [r for r in self.requests if r.method == method.upper() and r.url.path == self.prefix + path]

    # -- responses -------------------------------------------------------------------------------------------

    def _rid(self) -> str:
        self._counter += 1
        return f"req_mock{self._counter:04d}"

    def error(self, status: int, code: str, message: str, *, field_: Optional[str] = None, retry_after: Optional[str] = None,
              request_id: Optional[str] = None) -> httpx.Response:  # fmt: skip
        rid = request_id or self._rid()
        err: Dict[str, Any] = {"code": code, "message": message, "request_id": rid}
        if field_:
            err["field"] = field_
        headers = {"x-percia-request-id": rid, "content-type": "application/json"}
        if retry_after is not None:
            headers["retry-after"] = retry_after
        return httpx.Response(status, json={"error": err, "message": message, "request_id": rid}, headers=headers)

    def _scripted(self, s: Scripted, request: httpx.Request) -> httpx.Response:
        if isinstance(s, Exception):
            raise s
        if isinstance(s, Fail):
            if s.raw is not None:
                return httpx.Response(s.status, content=s.raw, headers={"x-percia-request-id": s.request_id or ""})
            return self.error(s.status, s.code, s.message, retry_after=s.retry_after, request_id=s.request_id)
        if isinstance(s, Json):
            return httpx.Response(s.status, json=s.body, headers={"x-percia-request-id": self._rid()})
        if isinstance(s, httpx.Response):
            return s
        return s(request)

    def handler(self, request: httpx.Request) -> httpx.Response:
        self.requests.append(request)
        method, path = request.method, request.url.path
        for m, rx, queue in self._scripts:
            if m == method and rx.match(path) and queue:
                return self._scripted(queue.pop(0), request)
        for m, rx, fn in self._custom:
            if m == method and rx.match(path):
                return fn(request)
        matches = [o for o in self._ops if o.regex.match(path)]
        if not matches:
            return self.error(404, "not_found", f"No route {path}")
        op = next((o for o in matches if o.method == method), None)
        if op is None:
            return self.error(405, "invalid_request", f"{method} not allowed on {path}")
        denied = self._check_auth(request, op)
        if denied is not None:
            return denied
        bad = self._check_body(request, op)
        if bad is not None:
            return bad
        return self._default(op)

    def _check_auth(self, request: httpx.Request, op: _Op) -> Optional[httpx.Response]:
        security = op.op.get("security") or []
        if not security:
            return None  # public
        bearer = [s["bearerAuth"] for s in security if "bearerAuth" in s]
        header = request.headers.get("authorization", "")
        if not bearer:  # session only: a key is refused
            return self.error(401, "unauthenticated", "Sign in to use this route.")
        if not header.lower().startswith("bearer "):
            return self.error(401, "unauthenticated", "Missing credential.")
        token = header[7:].strip()
        if token not in self.keys:
            return self.error(401, "invalid_api_key", "Invalid or revoked API key.")
        need = op.op.get("x-percia-scopes") or bearer[0]
        missing = [s for s in need if s not in self.keys[token]]
        if missing:
            return self.error(403, "insufficient_scope", f"This key needs the scope {missing[0]}.")
        return None

    def _check_body(self, request: httpx.Request, op: _Op) -> Optional[httpx.Response]:
        rb = op.op.get("requestBody")
        if not rb:
            return None
        schema = _resolve(self.spec, rb["content"]["application/json"]["schema"])
        try:
            body = json.loads(request.content or b"null")
        except ValueError:
            return self.error(400, "invalid_request", "Body is not JSON.")
        if not isinstance(body, dict):
            return self.error(400, "invalid_request", "Body must be an object.")
        for req in schema.get("required", []):
            if req not in body:
                return self.error(400, "invalid_request", f"{req} is required.", field_=req)
        return None

    def _default(self, op: _Op) -> httpx.Response:
        responses = op.op["responses"]
        status = min((int(s) for s in responses if s.isdigit() and s.startswith("2")), default=200)
        resp = responses.get(str(status), {})
        content = (resp.get("content") or {}).get("application/json")
        headers = {"x-percia-request-id": self._rid()}
        if content is None:
            return httpx.Response(status, headers=headers)
        body = content["example"] if "example" in content else instance(self.spec, content.get("schema", {}))
        return httpx.Response(status, json=body, headers=headers)
