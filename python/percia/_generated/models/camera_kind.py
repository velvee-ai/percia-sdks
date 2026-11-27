from enum import Enum


class CameraKind(str, Enum):
    FILE = "file"
    LINK = "link"
    PHONE = "phone"
    PUSH = "push"

    def __str__(self) -> str:
        return str(self.value)
