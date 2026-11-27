from enum import Enum


class SendEventFeedbackResponse200EngineType0State(str, Enum):
    APPLIED = "applied"
    RECORDED = "recorded"

    def __str__(self) -> str:
        return str(self.value)
