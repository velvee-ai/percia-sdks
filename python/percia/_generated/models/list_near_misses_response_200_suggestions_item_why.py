from enum import Enum


class ListNearMissesResponse200SuggestionsItemWhy(str, Enum):
    CLOSE_CALL = "close_call"
    FALSE_ALARM = "false_alarm"
    REPORTED_MISS = "reported_miss"

    def __str__(self) -> str:
        return str(self.value)
