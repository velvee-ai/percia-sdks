from enum import Enum


class GetCameraStatusResponse200Kind(str, Enum):
    PHONE = "phone"
    PUSH = "push"

    def __str__(self) -> str:
        return str(self.value)
