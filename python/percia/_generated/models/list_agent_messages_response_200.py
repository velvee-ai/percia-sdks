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
    from ..models.list_agent_messages_response_200_messages_item import (
        ListAgentMessagesResponse200MessagesItem,
    )


T = TypeVar("T", bound="ListAgentMessagesResponse200")


@_attrs_define
class ListAgentMessagesResponse200:
    """
    Attributes:
        messages (Union[Unset, list['ListAgentMessagesResponse200MessagesItem']]):
    """

    messages: Union[Unset, list["ListAgentMessagesResponse200MessagesItem"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        messages: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.messages, Unset):
            messages = []
            for messages_item_data in self.messages:
                messages_item = messages_item_data.to_dict()
                messages.append(messages_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if messages is not UNSET:
            field_dict["messages"] = messages

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.list_agent_messages_response_200_messages_item import (
            ListAgentMessagesResponse200MessagesItem,
        )

        d = dict(src_dict)
        messages = []
        _messages = d.pop("messages", UNSET)
        for messages_item_data in _messages or []:
            messages_item = ListAgentMessagesResponse200MessagesItem.from_dict(messages_item_data)

            messages.append(messages_item)

        list_agent_messages_response_200 = cls(
            messages=messages,
        )

        list_agent_messages_response_200.additional_properties = d
        return list_agent_messages_response_200

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
