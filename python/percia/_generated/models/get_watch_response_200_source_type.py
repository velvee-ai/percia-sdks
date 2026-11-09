from enum import Enum


class GetWatchResponse200SourceType(str, Enum):
    PHONE = "phone"
    RTSP = "rtsp"
    VIDEO = "video"

    def __str__(self) -> str:
        return str(self.value)
