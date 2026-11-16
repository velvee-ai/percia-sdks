from enum import Enum


class GetPlanResponse200BlockReasonType1(str, Enum):
    NEEDS_BILLING = "needs_billing"
    SPEND_CAP = "spend_cap"

    def __str__(self) -> str:
        return str(self.value)
