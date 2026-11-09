from enum import Enum


class CreateWatchResponse201LastDeliveryType1(str, Enum):
    DELIVERED = "delivered"
    FAILED = "failed"

    def __str__(self) -> str:
        return str(self.value)
