from enum import Enum


class UpdateWatchBodyAdvancedActionsItemKind(str, Enum):
    ADJUST_RECOMMENDED = "adjust_recommended"
    INSPECT_RECOMMENDED = "inspect_recommended"
    PAUSE_RECOMMENDED = "pause_recommended"
    RESUME_OK = "resume_ok"
    STOP_RECOMMENDED = "stop_recommended"

    def __str__(self) -> str:
        return str(self.value)
