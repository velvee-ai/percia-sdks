from enum import Enum


class HookCreatedEventsItem(str, Enum):
    GOAL_MET = "goal.met"
    VALUE_1 = "*"

    def __str__(self) -> str:
        return str(self.value)
