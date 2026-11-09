from enum import Enum


class CreateWatchResponse201DisplayStatus(str, Enum):
    ACTIVE = "active"
    ATTENTION = "attention"
    PAUSED = "paused"

    def __str__(self) -> str:
        return str(self.value)
