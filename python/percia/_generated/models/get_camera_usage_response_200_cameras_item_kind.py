from enum import Enum


class GetCameraUsageResponse200CamerasItemKind(str, Enum):
    LINK = "link"
    PHONE = "phone"
    REMOVED = "removed"

    def __str__(self) -> str:
        return str(self.value)
