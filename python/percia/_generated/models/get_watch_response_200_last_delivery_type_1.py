from enum import Enum


class GetWatchResponse200LastDeliveryType1(str, Enum):
    DELIVERED = "delivered"
    FAILED = "failed"

    def __str__(self) -> str:
        return str(self.value)
