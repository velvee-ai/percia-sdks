from enum import Enum


class StartTestRunBodySource(str, Enum):
    DATASET = "dataset"
    RECENT = "recent"
    WINDOW = "window"

    def __str__(self) -> str:
        return str(self.value)
