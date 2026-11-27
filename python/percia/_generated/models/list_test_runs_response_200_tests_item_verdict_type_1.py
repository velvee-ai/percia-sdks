from enum import Enum


class ListTestRunsResponse200TestsItemVerdictType1(str, Enum):
    READY = "ready"
    REVIEW = "review"
    UNMEASURED = "unmeasured"

    def __str__(self) -> str:
        return str(self.value)
