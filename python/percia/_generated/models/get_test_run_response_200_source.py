from enum import Enum


class GetTestRunResponse200Source(str, Enum):
    DATASET = "dataset"
    RECENT = "recent"
    UPLOAD = "upload"
    WINDOW = "window"

    def __str__(self) -> str:
        return str(self.value)
