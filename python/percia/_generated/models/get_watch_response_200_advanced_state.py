from enum import Enum


class GetWatchResponse200AdvancedState(str, Enum):
    PENDING = "pending"
    READY = "ready"

    def __str__(self) -> str:
        return str(self.value)
