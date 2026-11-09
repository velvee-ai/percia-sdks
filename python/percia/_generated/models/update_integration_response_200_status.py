from enum import Enum


class UpdateIntegrationResponse200Status(str, Enum):
    ACTIVE = "active"
    BROKEN = "broken"

    def __str__(self) -> str:
        return str(self.value)
