from enum import Enum


class GetConnectLinkResponse200ConnectKind(str, Enum):
    DEEPLINK = "deeplink"
    FIELDS = "fields"
    KEY = "key"
    OAUTH = "oauth"
    URL = "url"

    def __str__(self) -> str:
        return str(self.value)
