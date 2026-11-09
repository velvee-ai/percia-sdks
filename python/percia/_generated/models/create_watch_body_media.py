from enum import Enum


class CreateWatchBodyMedia(str, Enum):
    KEYFRAMES = "keyframes"
    OFF = "off"

    def __str__(self) -> str:
        return str(self.value)
