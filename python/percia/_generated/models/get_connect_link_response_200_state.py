from enum import Enum


class GetConnectLinkResponse200State(str, Enum):
    CONNECTED = "connected"
    EXPIRED = "expired"
    READY = "ready"
    UNKNOWN = "unknown"
    USED = "used"
    WRONG_USER = "wrong_user"

    def __str__(self) -> str:
        return str(self.value)
