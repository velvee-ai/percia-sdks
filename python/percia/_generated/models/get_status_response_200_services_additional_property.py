from enum import Enum


class GetStatusResponse200ServicesAdditionalProperty(str, Enum):
    DEGRADED = "degraded"
    DOWN = "down"
    OK = "ok"
    UNKNOWN = "unknown"

    def __str__(self) -> str:
        return str(self.value)
