from enum import Enum


class GetWatchResponse200NotifyType(str, Enum):
    EMAIL = "email"
    WEBHOOK = "webhook"

    def __str__(self) -> str:
        return str(self.value)
