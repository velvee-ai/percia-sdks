from enum import Enum


class CreateWatchResponse201AdvancedState(str, Enum):
    PENDING = "pending"
    READY = "ready"

    def __str__(self) -> str:
        return str(self.value)
