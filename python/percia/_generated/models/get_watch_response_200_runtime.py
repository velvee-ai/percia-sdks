from enum import Enum


class GetWatchResponse200Runtime(str, Enum):
    POOL = "pool"

    def __str__(self) -> str:
        return str(self.value)
