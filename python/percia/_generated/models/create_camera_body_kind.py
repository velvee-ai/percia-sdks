from enum import Enum


class CreateCameraBodyKind(str, Enum):
    PHONE = "phone"
    PUSH = "push"

    def __str__(self) -> str:
        return str(self.value)
