from enum import Enum


class TestRunResultsItemExpected(str, Enum):
    MET = "met"
    NOT_MET = "not_met"

    def __str__(self) -> str:
        return str(self.value)
