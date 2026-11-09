from enum import Enum


class AgentConfigConcernsItemKind(str, Enum):
    EVENT = "event"
    STATE = "state"

    def __str__(self) -> str:
        return str(self.value)
