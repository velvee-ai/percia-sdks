from enum import Enum


class CreatePublicWatchResponse201NotifyType(str, Enum):
    EMAIL = "email"

    def __str__(self) -> str:
        return str(self.value)
