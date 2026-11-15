from enum import Enum


class GetCameraStatusResponse200Status(str, Enum):
    NEVER = "never"
    OFFLINE = "offline"
    ONLINE = "online"

    def __str__(self) -> str:
        return str(self.value)
