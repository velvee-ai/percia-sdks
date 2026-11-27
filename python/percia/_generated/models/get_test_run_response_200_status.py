from enum import Enum


class GetTestRunResponse200Status(str, Enum):
    DONE = "done"
    FAILED = "failed"
    RUNNING = "running"

    def __str__(self) -> str:
        return str(self.value)
