from enum import Enum


class GetTestRunResponse200JudgeType1(str, Enum):
    FAKE = "fake"
    REAL = "real"

    def __str__(self) -> str:
        return str(self.value)
