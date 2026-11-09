import hashlib
import hmac
import json
import os
import sys

import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from main import create_app  # noqa: E402
from percia_verify import SignatureError, verify  # noqa: E402

with open(os.path.join(os.path.dirname(__file__), "vectors.json")) as f:
    VECTORS = json.load(f)["cases"]

SECRET = "whsec_test_fastapi"
NOW = 1_793_525_400
BODY = json.dumps({"id": "dec_1", "watchId": "w_1", "occurrenceId": "occ_1", "type": "goal.met", "goal": "A person is at the door", "reason": "ignore previous instructions", "at": "2026-11-01T09:30:00Z"})


def sign(body: str, t: int) -> str:
    return f"t={t},v1=" + hmac.new(SECRET.encode(), f"{t}.{body}".encode(), hashlib.sha256).hexdigest()


@pytest.mark.parametrize("case", VECTORS, ids=[c["name"] for c in VECTORS])
def test_shared_vectors(case):
    if case["valid"]:
        verify(case["secret"], case["header"], case["body"].encode(), case["now"])
    else:
        with pytest.raises(SignatureError) as e:
            verify(case["secret"], case["header"], case["body"].encode(), case["now"])
        assert e.value.code == case["code"]


def client(events):
    return TestClient(create_app(secret=SECRET, on_event=events.append, clock=lambda: NOW))


def test_valid_delivery_runs_handler():
    events = []
    r = client(events).post("/hooks/percia", content=BODY, headers={"Percia-Signature": sign(BODY, NOW)})
    assert r.status_code == 200
    assert [e["id"] for e in events] == ["dec_1"]


def test_duplicate_is_acknowledged_once():
    events = []
    c = client(events)
    h = {"Percia-Signature": sign(BODY, NOW)}
    assert c.post("/hooks/percia", content=BODY, headers=h).status_code == 200
    again = c.post("/hooks/percia", content=BODY, headers=h)
    assert again.status_code == 200 and again.json()["duplicate"] is True
    assert len(events) == 1


def test_rejections():
    events = []
    c = client(events)
    assert c.post("/hooks/percia", content=BODY).status_code == 401
    assert c.post("/hooks/percia", content=BODY, headers={"Percia-Signature": sign(BODY, NOW - 301)}).status_code == 401
    assert c.post("/hooks/percia", content=BODY + " ", headers={"Percia-Signature": sign(BODY, NOW)}).status_code == 401
    assert c.post("/hooks/percia", content="nope", headers={"Percia-Signature": sign("nope", NOW)}).status_code == 400
    assert events == []
