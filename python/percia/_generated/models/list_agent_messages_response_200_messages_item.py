import datetime
from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.list_agent_messages_response_200_messages_item_role import (
    ListAgentMessagesResponse200MessagesItemRole,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="ListAgentMessagesResponse200MessagesItem")


@_attrs_define
class ListAgentMessagesResponse200MessagesItem:
    """
    Attributes:
        created_at (Union[Unset, datetime.datetime]):
        id (Union[Unset, str]):
        role (Union[Unset, ListAgentMessagesResponse200MessagesItemRole]):
        text (Union[Unset, str]):
    """

    created_at: Union[Unset, datetime.datetime] = UNSET
    id: Union[Unset, str] = UNSET
    role: Union[Unset, ListAgentMessagesResponse200MessagesItemRole] = UNSET
    text: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        created_at: Union[Unset, str] = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()

        id = self.id

        role: Union[Unset, str] = UNSET
        if not isinstance(self.role, Unset):
            role = self.role.value

        text = self.text

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if created_at is not UNSET:
            field_dict["createdAt"] = created_at
        if id is not UNSET:
            field_dict["id"] = id
        if role is not UNSET:
            field_dict["role"] = role
        if text is not UNSET:
            field_dict["text"] = text

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _created_at = d.pop("createdAt", UNSET)
        created_at: Union[Unset, datetime.datetime]
        if isinstance(_created_at, Unset):
            created_at = UNSET
        else:
            created_at = isoparse(_created_at)

        id = d.pop("id", UNSET)

        _role = d.pop("role", UNSET)
        role: Union[Unset, ListAgentMessagesResponse200MessagesItemRole]
        if isinstance(_role, Unset):
            role = UNSET
        else:
            role = ListAgentMessagesResponse200MessagesItemRole(_role)

        text = d.pop("text", UNSET)

        list_agent_messages_response_200_messages_item = cls(
            created_at=created_at,
            id=id,
            role=role,
            text=text,
        )

        list_agent_messages_response_200_messages_item.additional_properties = d
        return list_agent_messages_response_200_messages_item

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
