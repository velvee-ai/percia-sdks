from enum import Enum


class GetPlanResponse200Plan(str, Enum):
    FREE = "free"
    PRO = "pro"

    def __str__(self) -> str:
        return str(self.value)
