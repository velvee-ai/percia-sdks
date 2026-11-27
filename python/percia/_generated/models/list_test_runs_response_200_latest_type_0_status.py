from enum import Enum


class ListTestRunsResponse200LatestType0Status(str, Enum):
    DONE = "done"
    FAILED = "failed"
    RUNNING = "running"

    def __str__(self) -> str:
        return str(self.value)
