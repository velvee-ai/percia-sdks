from enum import Enum


class CreateAgentBodyConfigConcernsItemKind(str, Enum):
    EVENT = "event"
    STATE = "state"

    def __str__(self) -> str:
        return str(self.value)
