from enum import Enum


class UpdateDatasetClipResponse200ClipLabel(str, Enum):
    COUNTERFACTUAL = "counterfactual"
    SHOULD_MATCH = "should_match"
    SHOULD_NOT = "should_not"

    def __str__(self) -> str:
        return str(self.value)
