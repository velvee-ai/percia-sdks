from enum import Enum


class AddDatasetClipFromEventResponse201ClipOrigin(str, Enum):
    EVENT = "event"
    MARK = "mark"
    NEAR_MISS = "near_miss"
    UPLOAD = "upload"

    def __str__(self) -> str:
        return str(self.value)
