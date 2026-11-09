from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.agent_config_actions_item_type import AgentConfigActionsItemType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.agent_config_actions_item_arguments import (
        AgentConfigActionsItemArguments,
    )
    from ..models.agent_config_actions_item_secret_header import (
        AgentConfigActionsItemSecretHeader,
    )


T = TypeVar("T", bound="AgentConfigActionsItem")


@_attrs_define
class AgentConfigActionsItem:
    """
    Attributes:
        on (str): "*" or a concern id.
        server_url (str): Public https URL of a streamable-HTTP MCP server.
        tool (str):
        type_ (AgentConfigActionsItemType):
        arguments (Union[Unset, AgentConfigActionsItemArguments]):
        secret_header (Union[Unset, AgentConfigActionsItemSecretHeader]):
    """

    on: str
    server_url: str
    tool: str
    type_: AgentConfigActionsItemType
    arguments: Union[Unset, "AgentConfigActionsItemArguments"] = UNSET
    secret_header: Union[Unset, "AgentConfigActionsItemSecretHeader"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        on = self.on

        server_url = self.server_url

        tool = self.tool

        type_ = self.type_.value

        arguments: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.arguments, Unset):
            arguments = self.arguments.to_dict()

        secret_header: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.secret_header, Unset):
            secret_header = self.secret_header.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "on": on,
                "serverUrl": server_url,
                "tool": tool,
                "type": type_,
            }
        )
        if arguments is not UNSET:
            field_dict["arguments"] = arguments
        if secret_header is not UNSET:
            field_dict["secretHeader"] = secret_header

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.agent_config_actions_item_arguments import (
            AgentConfigActionsItemArguments,
        )
        from ..models.agent_config_actions_item_secret_header import (
            AgentConfigActionsItemSecretHeader,
        )

        d = dict(src_dict)
        on = d.pop("on")

        server_url = d.pop("serverUrl")

        tool = d.pop("tool")

        type_ = AgentConfigActionsItemType(d.pop("type"))

        _arguments = d.pop("arguments", UNSET)
        arguments: Union[Unset, AgentConfigActionsItemArguments]
        if isinstance(_arguments, Unset):
            arguments = UNSET
        else:
            arguments = AgentConfigActionsItemArguments.from_dict(_arguments)

        _secret_header = d.pop("secretHeader", UNSET)
        secret_header: Union[Unset, AgentConfigActionsItemSecretHeader]
        if isinstance(_secret_header, Unset):
            secret_header = UNSET
        else:
            secret_header = AgentConfigActionsItemSecretHeader.from_dict(_secret_header)

        agent_config_actions_item = cls(
            on=on,
            server_url=server_url,
            tool=tool,
            type_=type_,
            arguments=arguments,
            secret_header=secret_header,
        )

        agent_config_actions_item.additional_properties = d
        return agent_config_actions_item

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
