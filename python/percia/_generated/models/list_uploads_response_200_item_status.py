from enum import Enum


class ListUploadsResponse200ItemStatus(str, Enum):
    FAILED = "failed"
    READY = "ready"
    UPLOADING = "uploading"

    def __str__(self) -> str:
        return str(self.value)
