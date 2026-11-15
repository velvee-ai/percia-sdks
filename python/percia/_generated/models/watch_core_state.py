from enum import Enum


class WatchCoreState(str, Enum):
    ABSENT = "absent"
    CONFIGURING = "configuring"
    DEGRADED = "degraded"
    ERROR = "error"
    OFF = "off"
    PENDING = "pending"
    RUNNING = "running"
    STOPPED = "stopped"

    def __str__(self) -> str:
        return str(self.value)
