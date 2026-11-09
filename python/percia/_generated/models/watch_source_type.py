from enum import Enum


class WatchSourceType(str, Enum):
    PHONE = "phone"
    RTSP = "rtsp"
    VIDEO = "video"

    def __str__(self) -> str:
        return str(self.value)
