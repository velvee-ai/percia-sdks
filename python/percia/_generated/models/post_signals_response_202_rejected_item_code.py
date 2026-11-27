from enum import Enum


class PostSignalsResponse202RejectedItemCode(str, Enum):
    INVALID_SIGNAL = "invalid_signal"
    INVALID_TARGET = "invalid_target"
    RATE_LIMITED = "rate_limited"
    TOO_OLD = "too_old"
    UNKNOWN_TARGET = "unknown_target"

    def __str__(self) -> str:
        return str(self.value)
