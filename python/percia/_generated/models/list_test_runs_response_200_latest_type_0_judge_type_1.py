from enum import Enum


class ListTestRunsResponse200LatestType0JudgeType1(str, Enum):
    FAKE = "fake"
    REAL = "real"

    def __str__(self) -> str:
        return str(self.value)
