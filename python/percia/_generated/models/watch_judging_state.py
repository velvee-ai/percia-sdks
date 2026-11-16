from enum import Enum


class WatchJudgingState(str, Enum):
    JUDGE_UNAVAILABLE = "judge_unavailable"
    JUDGING = "judging"
    NOT_RUNNING = "not_running"
    NO_VIDEO = "no_video"
    OVER_BUDGET = "over_budget"
    PAUSED = "paused"
    STARTING = "starting"
    UNKNOWN = "unknown"
    WAITING_FOR_CHANGE = "waiting_for_change"

    def __str__(self) -> str:
        return str(self.value)
