from enum import Enum


class ConnectionStatus(str, Enum):
    ACTIVE = "active"
    BROKEN = "broken"

    def __str__(self) -> str:
        return str(self.value)
