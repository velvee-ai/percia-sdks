from enum import Enum


class BuildAgentResponse201Degraded(str, Enum):
    PLAN_UNCHECKED = "plan_unchecked"
    REVIEW_SKIPPED = "review_skipped"

    def __str__(self) -> str:
        return str(self.value)
