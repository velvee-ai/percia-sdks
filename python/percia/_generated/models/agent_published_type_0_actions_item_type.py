from enum import Enum


class AgentPublishedType0ActionsItemType(str, Enum):
    MCP = "mcp"

    def __str__(self) -> str:
        return str(self.value)
