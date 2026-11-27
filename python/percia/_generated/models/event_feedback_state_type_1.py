from enum import Enum


class EventFeedbackStateType1(str, Enum):
    APPLIED = "applied"
    RECORDED = "recorded"

    def __str__(self) -> str:
        return str(self.value)
