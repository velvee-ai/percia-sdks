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
    from ..models.agent_config import AgentConfig


T = TypeVar("T", bound="ChatWithAgentResponse200")


@_attrs_define
class ChatWithAgentResponse200:
    """
    Attributes:
        changed (Union[Unset, bool]):
        draft (Union[Unset, AgentConfig]): Up to 10 concerns plus a request budget. A watch runs at most 8 concerns,
            without zones, excludeZones, minConfidence, rearmS, recheckS, cooldownS or a non-default budget (422
            agent_deploy_unavailable on deploy). A zone is a polygon of 3 to 12 [x, y] points, each 0..1 (fractions of the
            frame).
        reply (Union[Unset, str]):
    """

    changed: Union[Unset, bool] = UNSET
    draft: Union[Unset, "AgentConfig"] = UNSET
    reply: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        changed = self.changed

        draft: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.draft, Unset):
            draft = self.draft.to_dict()

        reply = self.reply

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if changed is not UNSET:
            field_dict["changed"] = changed
        if draft is not UNSET:
            field_dict["draft"] = draft
        if reply is not UNSET:
            field_dict["reply"] = reply

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.agent_config import AgentConfig

        d = dict(src_dict)
        changed = d.pop("changed", UNSET)

        _draft = d.pop("draft", UNSET)
        draft: Union[Unset, AgentConfig]
        if isinstance(_draft, Unset):
            draft = UNSET
        else:
            draft = AgentConfig.from_dict(_draft)

        reply = d.pop("reply", UNSET)

        chat_with_agent_response_200 = cls(
            changed=changed,
            draft=draft,
            reply=reply,
        )

        chat_with_agent_response_200.additional_properties = d
        return chat_with_agent_response_200

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
