from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.watch_notify_type import WatchNotifyType
from ..types import UNSET, Unset

T = TypeVar("T", bound="WatchNotify")


@_attrs_define
class WatchNotify:
    """
    Attributes:
        target (Union[Unset, str]):
        type_ (Union[Unset, WatchNotifyType]):
    """

    target: Union[Unset, str] = UNSET
    type_: Union[Unset, WatchNotifyType] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        target = self.target

        type_: Union[Unset, str] = UNSET
        if not isinstance(self.type_, Unset):
            type_ = self.type_.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if target is not UNSET:
            field_dict["target"] = target
        if type_ is not UNSET:
            field_dict["type"] = type_

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        target = d.pop("target", UNSET)

        _type_ = d.pop("type", UNSET)
        type_: Union[Unset, WatchNotifyType]
        if isinstance(_type_, Unset):
            type_ = UNSET
        else:
            type_ = WatchNotifyType(_type_)

        watch_notify = cls(
            target=target,
            type_=type_,
        )

        watch_notify.additional_properties = d
        return watch_notify

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
