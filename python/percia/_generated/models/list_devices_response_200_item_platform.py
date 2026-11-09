from enum import Enum


class ListDevicesResponse200ItemPlatform(str, Enum):
    IOS = "ios"

    def __str__(self) -> str:
        return str(self.value)
