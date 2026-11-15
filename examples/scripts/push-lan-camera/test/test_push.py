"""Offline end-to-end for push.py: a mock Percia API (the recorded contract) + a fake ffmpeg. Run: pytest -q"""

import json
import os
import stat
import subprocess
import sys
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[4]
CONTRACT = json.loads((ROOT / "spec" / "camera-push-contract.json").read_text())
TOKEN = CONTRACT["register"]["created"]["body"]["token"]
SCRIPT = Path(__file__).resolve().parents[1] / "push.py"

pytest.importorskip("percia")


def serve(existing: bool):
    calls = []

    class H(BaseHTTPRequestHandler):
        def log_message(self, *a):  # noqa: ANN002
            pass

        def _do(self):
            n = int(self.headers.get("content-length") or 0)
            body = json.loads(self.rfile.read(n)) if n else None
            calls.append({"method": self.command, "path": self.path, "auth": self.headers.get("authorization"), "body": body})
            if self.path == "/api/cameras" and self.command == "POST":
                out = CONTRACT["register"]["existing" if existing else "created"]
            elif self.path.endswith("/token"):
                out = CONTRACT["rotate"]
            elif self.path == "/api/cam/heartbeat":
                self.send_response(204)
                self.end_headers()
                return
            else:
                out = {"status": 404, "body": {"error": {"code": "not_found", "message": "x"}}}
            self.send_response(out["status"])
            self.send_header("content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(out["body"]).encode())

        do_POST = do_GET = _do

    srv = HTTPServer(("127.0.0.1", 0), H)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv, calls


def run(srv, tmp_path, **extra):
    fake = tmp_path / "ffmpeg"
    fake.write_text(f'#!/bin/sh\nprintf \'%s\\n\' "$@" > "{tmp_path}/argv.txt"\necho "WHIP ok token {TOKEN}" >&2\n')
    fake.chmod(fake.stat().st_mode | stat.S_IEXEC)
    env = {
        **os.environ,
        "PERCIA_API_KEY": "pk_live_test",
        "PERCIA_BASE_URL": f"http://127.0.0.1:{srv.server_port}",
        "RTSP_URL": "rtsp://admin:s3cret@192.168.1.20/s1",
        "FFMPEG": str(fake),
        "TOKEN_FILE": str(tmp_path / "token"),
        "ONCE": "1",
        "PYTHONPATH": str(ROOT / "python"),
        **extra,
    }
    return subprocess.run([sys.executable, "-I", str(SCRIPT)], env=env, cwd=tmp_path, capture_output=True, text=True)


def test_registers_saves_token_runs_ffmpeg_and_never_prints_secrets(tmp_path):
    srv, calls = serve(False)
    try:
        r = run(srv, tmp_path)
    finally:
        srv.shutdown()
    assert r.returncode == 0, r.stderr
    assert calls[0]["body"]["kind"] == "push"
    assert (tmp_path / "token").read_text().strip() == TOKEN
    assert (tmp_path / "token").stat().st_mode & 0o777 == 0o600
    argv = (tmp_path / "argv.txt").read_text().split("\n")
    assert TOKEN in argv and "whip" in argv
    assert TOKEN not in r.stderr and "s3cret" not in r.stderr and "[token]" in r.stderr
    assert next(c for c in calls if c["path"] == "/api/cam/heartbeat")["auth"] == f"Bearer {TOKEN}"


def test_rerun_uses_saved_token_and_lost_token_is_explained(tmp_path):
    srv, _ = serve(True)
    try:
        lost = run(srv, tmp_path)
        assert lost.returncode == 1 and "ROTATE=1" in lost.stderr
        (tmp_path / "token").write_text(TOKEN + "\n")
        assert run(srv, tmp_path).returncode == 0
        other = tmp_path / "other"
        other.mkdir()
        assert run(srv, other, ROTATE="1").returncode == 0
    finally:
        srv.shutdown()
