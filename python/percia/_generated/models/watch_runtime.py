from enum import Enum


class WatchRuntime(str, Enum):
    POOL = "pool"

    def __str__(self) -> str:
        return str(self.value)
