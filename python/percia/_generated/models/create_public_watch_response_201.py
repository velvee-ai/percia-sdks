from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.create_public_watch_response_201_notify_type import (
    CreatePublicWatchResponse201NotifyType,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="CreatePublicWatchResponse201")


@_attrs_define
class CreatePublicWatchResponse201:
    """
    Attributes:
        emailed (Union[Unset, bool]):
        id (Union[Unset, str]):
        notify_type (Union[Unset, CreatePublicWatchResponse201NotifyType]):
    """

    emailed: Union[Unset, bool] = UNSET
    id: Union[Unset, str] = UNSET
    notify_type: Union[Unset, CreatePublicWatchResponse201NotifyType] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        emailed = self.emailed

        id = self.id

        notify_type: Union[Unset, str] = UNSET
        if not isinstance(self.notify_type, Unset):
            notify_type = self.notify_type.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if emailed is not UNSET:
            field_dict["emailed"] = emailed
        if id is not UNSET:
            field_dict["id"] = id
        if notify_type is not UNSET:
            field_dict["notifyType"] = notify_type

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        emailed = d.pop("emailed", UNSET)

        id = d.pop("id", UNSET)

        _notify_type = d.pop("notifyType", UNSET)
        notify_type: Union[Unset, CreatePublicWatchResponse201NotifyType]
        if isinstance(_notify_type, Unset):
            notify_type = UNSET
        else:
            notify_type = CreatePublicWatchResponse201NotifyType(_notify_type)

        create_public_watch_response_201 = cls(
            emailed=emailed,
            id=id,
            notify_type=notify_type,
        )

        create_public_watch_response_201.additional_properties = d
        return create_public_watch_response_201

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
