from enum import Enum


class SetGeminiKeyResponse200Provider(str, Enum):
    GEMINI = "gemini"

    def __str__(self) -> str:
        return str(self.value)
