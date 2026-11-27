from enum import Enum


class ListUploadsResponse200ItemCodecType1(str, Enum):
    AV1 = "av1"
    H264 = "h264"
    HEVC = "hevc"
    VP8 = "vp8"
    VP9 = "vp9"

    def __str__(self) -> str:
        return str(self.value)
