from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    Literal,
    TypeVar,
    Union,
    cast,
)

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.update_agent_body_config_actions_item_arguments import (
        UpdateAgentBodyConfigActionsItemArguments,
    )
    from ..models.update_agent_body_config_actions_item_secret_header import (
        UpdateAgentBodyConfigActionsItemSecretHeader,
    )


T = TypeVar("T", bound="UpdateAgentBodyConfigActionsItem")


@_attrs_define
class UpdateAgentBodyConfigActionsItem:
    """
    Attributes:
        on (Union[Literal['*'], str]):
        server_url (str):
        tool (str):
        type_ (Literal['mcp']):
        arguments (Union[Unset, UpdateAgentBodyConfigActionsItemArguments]):
        secret_header (Union[Unset, UpdateAgentBodyConfigActionsItemSecretHeader]):
    """

    on: Union[Literal["*"], str]
    server_url: str
    tool: str
    type_: Literal["mcp"]
    arguments: Union[Unset, "UpdateAgentBodyConfigActionsItemArguments"] = UNSET
    secret_header: Union[Unset, "UpdateAgentBodyConfigActionsItemSecretHeader"] = UNSET

    def to_dict(self) -> dict[str, Any]:
        on: Union[Literal["*"], str]
        on = self.on

        server_url = self.server_url

        tool = self.tool

        type_ = self.type_

        arguments: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.arguments, Unset):
            arguments = self.arguments.to_dict()

        secret_header: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.secret_header, Unset):
            secret_header = self.secret_header.to_dict()

        field_dict: dict[str, Any] = {}

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
        from ..models.update_agent_body_config_actions_item_arguments import (
            UpdateAgentBodyConfigActionsItemArguments,
        )
        from ..models.update_agent_body_config_actions_item_secret_header import (
            UpdateAgentBodyConfigActionsItemSecretHeader,
        )

        d = dict(src_dict)

        def _parse_on(data: object) -> Union[Literal["*"], str]:
            on_type_0 = cast(Literal["*"], data)
            if on_type_0 != "*":
                raise ValueError(f"on_type_0 must match const '*', got '{on_type_0}'")
            return on_type_0
            return cast(Union[Literal["*"], str], data)

        on = _parse_on(d.pop("on"))

        server_url = d.pop("serverUrl")

        tool = d.pop("tool")

        type_ = cast(Literal["mcp"], d.pop("type"))
        if type_ != "mcp":
            raise ValueError(f"type must match const 'mcp', got '{type_}'")

        _arguments = d.pop("arguments", UNSET)
        arguments: Union[Unset, UpdateAgentBodyConfigActionsItemArguments]
        if isinstance(_arguments, Unset):
            arguments = UNSET
        else:
            arguments = UpdateAgentBodyConfigActionsItemArguments.from_dict(_arguments)

        _secret_header = d.pop("secretHeader", UNSET)
        secret_header: Union[Unset, UpdateAgentBodyConfigActionsItemSecretHeader]
        if isinstance(_secret_header, Unset):
            secret_header = UNSET
        else:
            secret_header = UpdateAgentBodyConfigActionsItemSecretHeader.from_dict(_secret_header)

        update_agent_body_config_actions_item = cls(
            on=on,
            server_url=server_url,
            tool=tool,
            type_=type_,
            arguments=arguments,
            secret_header=secret_header,
        )

        return update_agent_body_config_actions_item
