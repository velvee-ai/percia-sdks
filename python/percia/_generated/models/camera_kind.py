from enum import Enum


class CameraKind(str, Enum):
    PHONE = "phone"
    PUSH = "push"

    def __str__(self) -> str:
        return str(self.value)
