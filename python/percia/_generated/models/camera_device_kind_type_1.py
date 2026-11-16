from enum import Enum


class CameraDeviceKindType1(str, Enum):
    COMPUTER = "computer"
    PHONE = "phone"
    TABLET = "tablet"

    def __str__(self) -> str:
        return str(self.value)
