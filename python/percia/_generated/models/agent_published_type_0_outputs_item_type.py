from enum import Enum


class AgentPublishedType0OutputsItemType(str, Enum):
    BOOLEAN = "boolean"
    ENUM = "enum"
    NUMBER = "number"
    STRING = "string"

    def __str__(self) -> str:
        return str(self.value)
