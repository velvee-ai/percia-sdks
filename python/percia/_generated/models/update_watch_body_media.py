from enum import Enum


class UpdateWatchBodyMedia(str, Enum):
    KEYFRAMES = "keyframes"
    OFF = "off"

    def __str__(self) -> str:
        return str(self.value)
