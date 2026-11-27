from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.complete_upload_body_parts_item import CompleteUploadBodyPartsItem


T = TypeVar("T", bound="CompleteUploadBody")


@_attrs_define
class CompleteUploadBody:
    """
    Attributes:
        parts (list['CompleteUploadBodyPartsItem']):
    """

    parts: list["CompleteUploadBodyPartsItem"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        parts = []
        for parts_item_data in self.parts:
            parts_item = parts_item_data.to_dict()
            parts.append(parts_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "parts": parts,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.complete_upload_body_parts_item import CompleteUploadBodyPartsItem

        d = dict(src_dict)
        parts = []
        _parts = d.pop("parts")
        for parts_item_data in _parts:
            parts_item = CompleteUploadBodyPartsItem.from_dict(parts_item_data)

            parts.append(parts_item)

        complete_upload_body = cls(
            parts=parts,
        )

        complete_upload_body.additional_properties = d
        return complete_upload_body

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
