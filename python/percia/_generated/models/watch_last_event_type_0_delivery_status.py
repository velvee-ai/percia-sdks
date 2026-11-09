from enum import Enum


class WatchLastEventType0DeliveryStatus(str, Enum):
    DELIVERED = "delivered"
    FAILED = "failed"
    PENDING = "pending"

    def __str__(self) -> str:
        return str(self.value)
