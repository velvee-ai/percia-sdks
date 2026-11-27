from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.add_dataset_clip_from_event_body_label import (
    AddDatasetClipFromEventBodyLabel,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="AddDatasetClipFromEventBody")


@_attrs_define
class AddDatasetClipFromEventBody:
    """
    Attributes:
        event_id (str):
        label (AddDatasetClipFromEventBodyLabel):
        note (Union[Unset, str]):
    """

    event_id: str
    label: AddDatasetClipFromEventBodyLabel
    note: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        event_id = self.event_id

        label = self.label.value

        note = self.note

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "eventId": event_id,
                "label": label,
            }
        )
        if note is not UNSET:
            field_dict["note"] = note

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        event_id = d.pop("eventId")

        label = AddDatasetClipFromEventBodyLabel(d.pop("label"))

        note = d.pop("note", UNSET)

        add_dataset_clip_from_event_body = cls(
            event_id=event_id,
            label=label,
            note=note,
        )

        add_dataset_clip_from_event_body.additional_properties = d
        return add_dataset_clip_from_event_body

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
