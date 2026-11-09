from enum import Enum


class CreateApiKeyResponse201ScopesItem(str, Enum):
    CAMERASREAD = "cameras:read"
    CAMERASWRITE = "cameras:write"
    DEVICESWRITE = "devices:write"
    EVENTSREAD = "events:read"
    INTEGRATIONSREAD = "integrations:read"
    INTEGRATIONSWRITE = "integrations:write"
    WATCHESDELETE = "watches:delete"
    WATCHESREAD = "watches:read"
    WATCHESWRITE = "watches:write"

    def __str__(self) -> str:
        return str(self.value)
