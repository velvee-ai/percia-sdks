from enum import Enum


class TestCaseType0Expected(str, Enum):
    MET = "met"
    NOT_MET = "not_met"

    def __str__(self) -> str:
        return str(self.value)
