from enum import Enum


class ListTestRunsResponse200TestsItemJudgeType1(str, Enum):
    FAKE = "fake"
    REAL = "real"

    def __str__(self) -> str:
        return str(self.value)
