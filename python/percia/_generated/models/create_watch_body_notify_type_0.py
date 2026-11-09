from collections.abc import Mapping
from typing import (
    Any,
    Literal,
    TypeVar,
    cast,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="CreateWatchBodyNotifyType0")


@_attrs_define
class CreateWatchBodyNotifyType0:
    """
    Attributes:
        target (str):
        type_ (Literal['email']):
    """

    target: str
    type_: Literal["email"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        target = self.target

        type_ = self.type_

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "target": target,
                "type": type_,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        target = d.pop("target")

        type_ = cast(Literal["email"], d.pop("type"))
        if type_ != "email":
            raise ValueError(f"type must match const 'email', got '{type_}'")

        create_watch_body_notify_type_0 = cls(
            target=target,
            type_=type_,
        )

        create_watch_body_notify_type_0.additional_properties = d
        return create_watch_body_notify_type_0

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
