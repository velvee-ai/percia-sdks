from enum import Enum


class GetCreditsResponse200GrantsItemSource(str, Enum):
    ADMIN = "admin"
    CODE = "code"

    def __str__(self) -> str:
        return str(self.value)
