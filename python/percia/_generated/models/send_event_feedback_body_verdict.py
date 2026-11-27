from enum import Enum


class SendEventFeedbackBodyVerdict(str, Enum):
    CORRECT = "correct"
    FALSE_ALARM = "false_alarm"
    PARTLY = "partly"

    def __str__(self) -> str:
        return str(self.value)
