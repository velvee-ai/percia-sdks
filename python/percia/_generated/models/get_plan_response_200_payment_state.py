from enum import Enum


class GetPlanResponse200PaymentState(str, Enum):
    ACTIVE = "active"
    BLOCKED = "blocked"
    GRACE = "grace"

    def __str__(self) -> str:
        return str(self.value)
