from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.agent import Agent


T = TypeVar("T", bound="BuildAgentResponse201")


@_attrs_define
class BuildAgentResponse201:
    """
    Attributes:
        agent (Union[Unset, Agent]):
        reply (Union[Unset, str]):
    """

    agent: Union[Unset, "Agent"] = UNSET
    reply: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        agent: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.agent, Unset):
            agent = self.agent.to_dict()

        reply = self.reply

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if agent is not UNSET:
            field_dict["agent"] = agent
        if reply is not UNSET:
            field_dict["reply"] = reply

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.agent import Agent

        d = dict(src_dict)
        _agent = d.pop("agent", UNSET)
        agent: Union[Unset, Agent]
        if isinstance(_agent, Unset):
            agent = UNSET
        else:
            agent = Agent.from_dict(_agent)

        reply = d.pop("reply", UNSET)

        build_agent_response_201 = cls(
            agent=agent,
            reply=reply,
        )

        build_agent_response_201.additional_properties = d
        return build_agent_response_201

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
