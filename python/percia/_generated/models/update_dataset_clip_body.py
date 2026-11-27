from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.update_dataset_clip_body_label import UpdateDatasetClipBodyLabel
from ..types import UNSET, Unset

T = TypeVar("T", bound="UpdateDatasetClipBody")


@_attrs_define
class UpdateDatasetClipBody:
    """
    Attributes:
        label (Union[Unset, UpdateDatasetClipBodyLabel]):
        note (Union[Unset, str]):
    """

    label: Union[Unset, UpdateDatasetClipBodyLabel] = UNSET
    note: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        label: Union[Unset, str] = UNSET
        if not isinstance(self.label, Unset):
            label = self.label.value

        note = self.note

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if label is not UNSET:
            field_dict["label"] = label
        if note is not UNSET:
            field_dict["note"] = note

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _label = d.pop("label", UNSET)
        label: Union[Unset, UpdateDatasetClipBodyLabel]
        if isinstance(_label, Unset):
            label = UNSET
        else:
            label = UpdateDatasetClipBodyLabel(_label)

        note = d.pop("note", UNSET)

        update_dataset_clip_body = cls(
            label=label,
            note=note,
        )

        update_dataset_clip_body.additional_properties = d
        return update_dataset_clip_body

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
