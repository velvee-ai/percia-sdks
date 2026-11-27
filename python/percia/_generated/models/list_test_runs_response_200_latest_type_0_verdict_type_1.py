from enum import Enum


class ListTestRunsResponse200LatestType0VerdictType1(str, Enum):
    READY = "ready"
    REVIEW = "review"
    UNMEASURED = "unmeasured"

    def __str__(self) -> str:
        return str(self.value)
