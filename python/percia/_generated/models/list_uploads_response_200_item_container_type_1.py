from enum import Enum


class ListUploadsResponse200ItemContainerType1(str, Enum):
    MKV = "mkv"
    MOV = "mov"
    MP4 = "mp4"
    WEBM = "webm"

    def __str__(self) -> str:
        return str(self.value)
