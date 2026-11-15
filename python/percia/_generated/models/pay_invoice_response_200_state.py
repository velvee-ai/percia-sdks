from enum import Enum


class PayInvoiceResponse200State(str, Enum):
    ACTIVE = "active"
    BLOCKED = "blocked"
    GRACE = "grace"

    def __str__(self) -> str:
        return str(self.value)
