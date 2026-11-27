from enum import Enum


class ReportMissResponse201EngineState(str, Enum):
    APPLIED = "applied"
    RECORDED = "recorded"

    def __str__(self) -> str:
        return str(self.value)
