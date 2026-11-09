from enum import Enum


class SiteRegion(str, Enum):
    EU = "eu"
    OTHER = "other"

    def __str__(self) -> str:
        return str(self.value)
