from enum import Enum


class GetCameraStatusResponse200State(str, Enum):
    OFFLINE = "offline"
    ONLINE = "online"
    REVOKED = "revoked"
    WAITING = "waiting"

    def __str__(self) -> str:
        return str(self.value)
