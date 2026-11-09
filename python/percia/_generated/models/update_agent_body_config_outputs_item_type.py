from enum import Enum


class UpdateAgentBodyConfigOutputsItemType(str, Enum):
    BOOLEAN = "boolean"
    ENUM = "enum"
    NUMBER = "number"
    STRING = "string"

    def __str__(self) -> str:
        return str(self.value)
