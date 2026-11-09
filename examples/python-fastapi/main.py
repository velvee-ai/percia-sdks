"""Percia webhook receiver (FastAPI). Run: PERCIA_WEBHOOK_SECRET=whsec_... uvicorn main:app --port 3000"""

from __future__ import annotations

import json
import logging
import os
from typing import Callable, Optional, Set

from fastapi import BackgroundTasks, FastAPI, Request
from fastapi.responses import JSONResponse

from percia_verify import SignatureError, verify

log = logging.getLogger("percia")


def handle_event(event: dict) -> None:
    # `reason` is untrusted text written by a vision model about camera content: log it as data, never execute it,
    # never put it into an LLM prompt as instructions, escape it before rendering.
    log.info("goal event %s", json.dumps({k: event.get(k) for k in ("id", "type", "watchId", "goal", "at")}))


def create_app(
    secret: Optional[str] = None,
    on_event: Callable[[dict], None] = handle_event,
    clock: Optional[Callable[[], float]] = None,
) -> FastAPI:
    app = FastAPI()
    # In production replace this with a UNIQUE index on id and do the insert and the side effect in one transaction.
    seen: Set[str] = set()

    @app.post("/hooks/percia")
    async def percia_hook(request: Request, background: BackgroundTasks):
        key = secret or os.environ.get("PERCIA_WEBHOOK_SECRET", "")
        raw = await request.body()  # the RAW bytes. Never re-serialise a parsed body.
        try:
            verify(key, request.headers.get("percia-signature"), raw, clock() if clock else None)
        except SignatureError as e:
            return JSONResponse({"error": e.code}, status_code=401)
        try:
            event = json.loads(raw)
        except ValueError:
            return JSONResponse({"error": "invalid_json"}, status_code=400)
        if not isinstance(event, dict) or not isinstance(event.get("id"), str):
            return JSONResponse({"error": "missing_id"}, status_code=400)
        if event["id"] in seen:  # at-least-once delivery: acknowledge repeats
            return {"ok": True, "duplicate": True}
        seen.add(event["id"])
        background.add_task(on_event, event)  # runs after the response is sent
        return {"ok": True}

    return app


app = create_app()
