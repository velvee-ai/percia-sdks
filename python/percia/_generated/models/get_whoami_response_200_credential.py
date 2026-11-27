from enum import Enum


class GetWhoamiResponse200Credential(str, Enum):
    KEY = "key"
    OAUTH = "oauth"
    SESSION = "session"

    def __str__(self) -> str:
        return str(self.value)
