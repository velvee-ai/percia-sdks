from enum import Enum


class CompleteUploadResponse200Status(str, Enum):
    FAILED = "failed"
    READY = "ready"
    UPLOADING = "uploading"

    def __str__(self) -> str:
        return str(self.value)
