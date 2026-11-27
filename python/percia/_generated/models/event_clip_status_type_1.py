from enum import Enum


class EventClipStatusType1(str, Enum):
    EVIDENCE_EXPIRED = "evidence_expired"
    PENDING = "pending"
    READY = "ready"

    def __str__(self) -> str:
        return str(self.value)
