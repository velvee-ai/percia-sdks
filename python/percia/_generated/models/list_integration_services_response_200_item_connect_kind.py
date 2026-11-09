from enum import Enum


class ListIntegrationServicesResponse200ItemConnectKind(str, Enum):
    DEEPLINK = "deeplink"
    OAUTH = "oauth"
    URL = "url"

    def __str__(self) -> str:
        return str(self.value)
