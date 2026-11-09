from enum import Enum


class WatchNotifyType(str, Enum):
    EMAIL = "email"
    WEBHOOK = "webhook"

    def __str__(self) -> str:
        return str(self.value)
