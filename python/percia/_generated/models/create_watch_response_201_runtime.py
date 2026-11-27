from enum import Enum


class CreateWatchResponse201Runtime(str, Enum):
    POOL = "pool"

    def __str__(self) -> str:
        return str(self.value)
