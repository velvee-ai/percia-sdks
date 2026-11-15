"""Push an RTSP camera on your LAN to Percia. Run it on a machine that can reach the camera.

    PERCIA_API_KEY=pk_live_... RTSP_URL=rtsp://user:pass@192.168.1.20/stream1 python push.py

Registers the camera (idempotent: running again reuses it), keeps the one-time publish token in .percia-camera-token
(mode 0600, never printed), then runs ffmpeg RTSP -> WHIP plus a heartbeat until Ctrl-C.
Needs ffmpeg 7.1+ with the whip muxer (check: ffmpeg -muxers | grep whip). The camera serves ONE RTSP session.
"""

from __future__ import annotations

import hashlib
import os
import subprocess
import sys
import threading
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

import httpx
from percia import Percia, publish_argv, scrub_token

env = os.environ
api_key, rtsp_url = env.get("PERCIA_API_KEY"), env.get("RTSP_URL")
if not api_key or not rtsp_url:
    sys.exit("Set PERCIA_API_KEY (scope cameras:write) and RTSP_URL (the camera's LAN address).")
base_url = env.get("PERCIA_BASE_URL", "https://playground.percia.ai").rstrip("/")
parts = urlsplit(rtsp_url)
hidden = urlunsplit(parts._replace(netloc=parts.netloc.rsplit("@", 1)[-1]))  # no credentials: safe to print
external_id = env.get("EXTERNAL_ID") or f"example-{parts.hostname}-{hashlib.sha256(hidden.encode()).hexdigest()[:6]}"
name = env.get("CAMERA_NAME", f"Camera {parts.hostname}")
token_file = Path(env.get("TOKEN_FILE", ".percia-camera-token"))
ffmpeg = env.get("FFMPEG", "ffmpeg")
mode = "transcode" if env.get("MODE") == "transcode" else "copy"


def save_token(value: str) -> None:
    token_file.write_text(value + "\n")
    token_file.chmod(0o600)


with Percia(api_key=api_key, base_url=base_url) as percia:
    # 1. Register. Idempotent by external_id: the first call returns the token, later calls return the camera and token None.
    reg = percia.cameras.register_push(name, external_id)
    token = reg.token
    if token:
        save_token(token)
        print(f"Registered camera {reg.camera.id}. The publish token (shown once) was saved to {token_file}.", file=sys.stderr)
    elif token_file.exists():
        token = token_file.read_text().strip()
        print(f"Camera {reg.camera.id} already registered; using the token in {token_file}.", file=sys.stderr)
    else:
        print(
            f"Camera {reg.camera.id} exists but there is no saved token, and Percia shows it only once.\n"
            "Mint a new one (it stops other publishers using the old one): ROTATE=1 python push.py",
            file=sys.stderr,
        )
        if env.get("ROTATE") != "1":
            sys.exit(1)
        token = percia.cameras.rotate_token(reg.camera.id).token
        save_token(token)
    assert token

# 2. Keep-alive: online means seen in the last 60 s.
stop = threading.Event()


def beat() -> None:
    try:
        httpx.post(f"{base_url}/api/cam/heartbeat", headers={"authorization": f"Bearer {token}"}, timeout=10)
    except httpx.HTTPError:
        pass


def heartbeat_loop() -> None:
    beat()
    while not stop.wait(20):
        beat()


beat()
threading.Thread(target=heartbeat_loop, daemon=True).start()

# 3. Publish: ffmpeg pulls the camera once and pushes it to the WHIP URL. Restart with backoff if it drops.
delay, code = 2.0, 0
try:
    while True:
        print(f"Pushing {hidden} -> {reg.whip_url}", file=sys.stderr)
        argv = [ffmpeg, "-hide_banner", "-loglevel", "warning", *publish_argv(reg.whip_url, token, rtsp_url, mode)]
        try:
            proc = subprocess.run(argv, stdin=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True)
        except FileNotFoundError:
            sys.exit(f"Cannot start {ffmpeg}. Install ffmpeg 7.1+ (with the whip muxer).")
        sys.stderr.write(scrub_token(proc.stderr or "", token))
        code = proc.returncode
        if env.get("ONCE") == "1":
            break
        print(f"ffmpeg exited ({code}); restarting in {delay:.0f}s", file=sys.stderr)
        if stop.wait(delay):
            break
        delay = min(delay * 2, 30.0)
except KeyboardInterrupt:
    code = 0
finally:
    stop.set()
sys.exit(code)
