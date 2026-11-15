from enum import Enum


class GetWatchResponse200Runtime(str, Enum):
    CORE = "core"
    POOL = "pool"

    def __str__(self) -> str:
        return str(self.value)
