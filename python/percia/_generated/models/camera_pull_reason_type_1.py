from enum import Enum


class CameraPullReasonType1(str, Enum):
    AUTH = "auth"
    KEYFRAME_INTERVAL = "keyframe_interval"
    OTHER = "other"
    PRIVATE_ADDRESS = "private_address"
    TIMEOUT = "timeout"
    UNREACHABLE = "unreachable"
    UNSUPPORTED_CODEC = "unsupported_codec"

    def __str__(self) -> str:
        return str(self.value)
