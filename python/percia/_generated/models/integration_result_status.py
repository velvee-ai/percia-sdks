from enum import Enum


class IntegrationResultStatus(str, Enum):
    DELIVERED = "delivered"
    FAILED = "failed"
    PENDING = "pending"
    RATE_LIMITED = "rate_limited"

    def __str__(self) -> str:
        return str(self.value)
