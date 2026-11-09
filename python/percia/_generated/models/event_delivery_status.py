from enum import Enum


class EventDeliveryStatus(str, Enum):
    DELIVERED = "delivered"
    FAILED = "failed"
    PENDING = "pending"

    def __str__(self) -> str:
        return str(self.value)
