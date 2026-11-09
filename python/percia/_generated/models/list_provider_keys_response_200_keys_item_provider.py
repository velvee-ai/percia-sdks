from enum import Enum


class ListProviderKeysResponse200KeysItemProvider(str, Enum):
    GEMINI = "gemini"

    def __str__(self) -> str:
        return str(self.value)
