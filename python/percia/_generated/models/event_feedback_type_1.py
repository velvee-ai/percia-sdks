from enum import Enum


class EventFeedbackType1(str, Enum):
    CORRECT = "correct"
    FALSE_ALARM = "false_alarm"
    PARTLY = "partly"

    def __str__(self) -> str:
        return str(self.value)
