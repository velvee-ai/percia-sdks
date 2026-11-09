from enum import Enum


class CameraStatus(str, Enum):
    NEVER = "never"
    OFFLINE = "offline"
    ONLINE = "online"

    def __str__(self) -> str:
        return str(self.value)
