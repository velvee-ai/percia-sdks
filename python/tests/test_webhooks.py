from __future__ import annotations

import hashlib
import hmac
import json
from pathlib import Path

import pytest

from percia import WebhookSignatureError, check_webhook_signature, verify_and_parse, verify_webhook_signature

VECTORS = json.loads((Path(__file__).resolve().parents[2] / "spec" / "webhook-vectors.json").read_text())
CASES = VECTORS["cases"]


def _id(c):  # type: ignore[no-untyped-def]
    return c["name"]


@pytest.mark.parametrize("case", CASES, ids=_id)
def test_vectors_with_header_string(case):  # type: ignore[no-untyped-def]
    got = verify_webhook_signature(
        case["body"].encode(), case["header"], case["secret"], VECTORS["tolerance_seconds"], now=case["now"]
    )
    assert got is case["valid"]


@pytest.mark.parametrize("case", CASES, ids=_id)
def test_vectors_report_the_documented_code(case):  # type: ignore[no-untyped-def]
    if case["valid"]:
        check_webhook_signature(case["body"], {"Percia-Signature": case["header"]}, case["secret"], now=case["now"])
        return
    with pytest.raises(WebhookSignatureError) as exc:
        check_webhook_signature(
            case["body"].encode(), {"percia-signature": case["header"]}, case["secret"], now=case["now"]
        )
    assert exc.value.code == case["code"]


@pytest.mark.parametrize(
    "make",
    [
        lambda h: {"Percia-Signature": h},
        lambda h: {"PERCIA-SIGNATURE": h},
        lambda h: {b"percia-signature": h.encode()},
        lambda h: [("x", "y")] and {"X-Other": "1", "percia-Signature": h},
        lambda h: h.encode(),
    ],
    ids=["canonical", "upper", "bytes-keys", "mixed-case", "bytes-value"],
)
def test_header_shapes(make):  # type: ignore[no-untyped-def]
    c = CASES[0]
    assert verify_webhook_signature(c["body"], make(c["header"]), c["secret"], now=c["now"])


def test_missing_header_is_malformed():
    with pytest.raises(WebhookSignatureError) as exc:
        check_webhook_signature("{}", {"Content-Type": "application/json"}, "whsec_x", now=1)
    assert exc.value.code == "malformed"
    assert verify_webhook_signature("{}", {}, "whsec_x") is False


def test_tolerance_is_configurable():
    c = CASES[0]
    t = int(c["header"].split(",")[0][2:])
    assert verify_webhook_signature(c["body"], c["header"], c["secret"], tolerance_sec=10, now=t + 11) is False
    assert verify_webhook_signature(c["body"], c["header"], c["secret"], tolerance_sec=3600, now=t + 3000) is True
    secret, body, ts = "whsec_x", b'{"a":1}', 1_700_000_000
    sig = hmac.new(secret.encode(), f"{ts}.".encode() + body, hashlib.sha256).hexdigest()
    header = f"t={ts},v1={sig}"
    assert verify_webhook_signature(body, header, secret, tolerance_sec=3600, now=ts + 3000)
    assert not verify_webhook_signature(body, header, secret, tolerance_sec=10, now=ts + 11)


def test_uses_current_time_by_default():
    import time

    secret, body = "whsec_live", b"{}"
    ts = int(time.time())
    sig = hmac.new(secret.encode(), f"{ts}.".encode() + body, hashlib.sha256).hexdigest()
    assert verify_webhook_signature(body, f"t={ts},v1={sig}", secret)
    assert not verify_webhook_signature(body, f"t={ts - 1000},v1={sig}", secret)


def test_verify_and_parse_returns_the_payload():
    c = CASES[0]
    payload = verify_and_parse(c["body"].encode(), {"Percia-Signature": c["header"]}, c["secret"], now=c["now"])
    assert payload["type"] == "goal.met" and payload["watchId"] == "w_abc"


def test_verify_and_parse_raises_before_parsing_bad_json():
    secret, body, ts = "whsec_x", b"not json", 1_700_000_000
    sig = hmac.new(secret.encode(), f"{ts}.".encode() + body, hashlib.sha256).hexdigest()
    with pytest.raises(ValueError):
        verify_and_parse(body, f"t={ts},v1={sig}", secret, now=ts)
    with pytest.raises(WebhookSignatureError) as exc:
        verify_and_parse(b"tampered", f"t={ts},v1={sig}", secret, now=ts)
    assert exc.value.code == "mismatch"


def test_non_ascii_signature_candidate_does_not_crash():
    assert verify_webhook_signature("{}", "t=1700000000,v1=ééé", "whsec_x", now=1_700_000_000) is False
