"""Camera push (cameras on a private network): the registration result and the helpers that turn it into publish commands.

The publish token is a bearer secret shown ONCE. Nothing here logs it: ``repr`` of a registration hides it, and the
printable commands use the placeholder ``$PERCIA_CAMERA_TOKEN``. Only ``publish_argv`` takes the real token, to spawn a process.
"""

from __future__ import annotations

import shlex
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

TOKEN_PLACEHOLDER = "$PERCIA_CAMERA_TOKEN"
TOKEN_ENV = "PERCIA_CAMERA_TOKEN"
_TRANSCODE_VF = "scale=-2:'min(ih,720)',fps=10,format=yuv420p"


@dataclass(frozen=True)
class PushRegistration:
    """Result of ``cameras.register_push``.

    * ``existing=False``: the camera was just created and ``token`` is the publish token, shown once. Store it now.
    * ``existing=True``: a camera with this ``external_id`` already existed (HTTP 200). The server never returns a token twice,
      so ``token`` is ``None`` unless you passed ``on_existing="rotate"`` (then it is a fresh token and the old one is dead).
    """

    camera: Any  # percia._generated.models.Camera
    whip_url: str
    token: Optional[str] = field(default=None, repr=False)
    existing: bool = False
    rotated: bool = False
    publish: Optional[Dict[str, Any]] = None

    def __repr__(self) -> str:  # never show the token, even to a stray print()
        t = "<hidden>" if self.token else None
        return (
            f"PushRegistration(camera_id={getattr(self.camera, 'id', None)!r}, whip_url={self.whip_url!r}, "
            f"token={t}, existing={self.existing}, rotated={self.rotated})"
        )

    __str__ = __repr__


def scrub_token(text: str, token: Optional[str]) -> str:
    """Replace every occurrence of the token in a text (child process output, error messages)."""
    return text.replace(token, "[token]") if token else text


def publish_argv(whip_url: str, token: str, rtsp: str, mode: str = "copy") -> List[str]:
    """ffmpeg arguments (an argv, no shell) for ``ffmpeg ... -f whip``. The token goes in as an argument: pass it only to spawn."""
    head = ["-re"] if mode == "transcode" else []
    video = (
        ["-vf", _TRANSCODE_VF, "-c:v", "libx264", "-profile:v", "baseline", "-preset", "veryfast", "-tune", "zerolatency",
         "-bf", "0", "-g", "20", "-b:v", "1500k", "-maxrate", "1500k", "-bufsize", "3000k"]
        if mode == "transcode"
        else ["-c:v", "copy"]
    )  # fmt: skip
    return [*head, "-rtsp_transport", "tcp", "-i", rtsp, "-an", *video, "-f", "whip", "-authorization", token, whip_url]


def build_publish_commands(
    whip_url: str, rtsp: str, mode: str = "copy", api_base: str = "https://playground.percia.ai"
) -> Dict[str, Any]:
    """Printable publish commands. The token never appears: they use ``$PERCIA_CAMERA_TOKEN``."""
    parts = []
    argv = publish_argv(whip_url, TOKEN_PLACEHOLDER, rtsp, mode)
    for i, a in enumerate(argv):
        parts.append(
            f'"{TOKEN_PLACEHOLDER}"' if a == TOKEN_PLACEHOLDER and argv[i - 1] == "-authorization" else shlex.quote(a)
        )
    api = api_base.rstrip("/")
    api = api[:-4] if api.endswith("/api") else api
    return {
        "ffmpeg": " ".join(["ffmpeg", *parts]),
        "obs": {
            "service": "WHIP",
            "server": whip_url,
            "bearer_token": TOKEN_PLACEHOLDER,
            "notes": [
                "Output: x264, keyframe interval 2 s, B-frames 0, CBR 1500 kbit/s, no audio is fine.",
                "OBS 30.2 or newer has the WHIP service.",
            ],
        },
        "gstreamer": (
            f"gst-launch-1.0 rtspsrc location={shlex.quote(rtsp)} protocols=tcp latency=200 ! rtph264depay ! h264parse ! "
            f'whipclientsink signaller::whip-endpoint={shlex.quote(whip_url)} signaller::auth-token="{TOKEN_PLACEHOLDER}"'
        ),
        "heartbeat": f'curl -fsS -X POST -H "Authorization: Bearer {TOKEN_PLACEHOLDER}" {api}/api/cam/heartbeat',
        "env": f"export {TOKEN_ENV}=<the token from registration>",
    }
