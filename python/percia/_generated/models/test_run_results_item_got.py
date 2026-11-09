from enum import Enum


class TestRunResultsItemGot(str, Enum):
    MET = "met"
    NOT_MET = "not_met"
    SKIPPED = "skipped"

    def __str__(self) -> str:
        return str(self.value)
