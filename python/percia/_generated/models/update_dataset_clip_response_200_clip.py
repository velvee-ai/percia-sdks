import datetime
from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
    cast,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.update_dataset_clip_response_200_clip_label import (
    UpdateDatasetClipResponse200ClipLabel,
)
from ..models.update_dataset_clip_response_200_clip_origin import (
    UpdateDatasetClipResponse200ClipOrigin,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="UpdateDatasetClipResponse200Clip")


@_attrs_define
class UpdateDatasetClipResponse200Clip:
    """
    Attributes:
        created_at (Union[Unset, datetime.datetime]):
        event_id (Union[None, Unset, str]):
        has_thumb (Union[Unset, bool]):
        id (Union[Unset, str]):
        label (Union[Unset, UpdateDatasetClipResponse200ClipLabel]):
        miss_id (Union[None, Unset, str]): Set for a clip kept from a reported miss.
        note (Union[Unset, str]):
        origin (Union[Unset, UpdateDatasetClipResponse200ClipOrigin]):
        seconds (Union[Unset, float]):
    """

    created_at: Union[Unset, datetime.datetime] = UNSET
    event_id: Union[None, Unset, str] = UNSET
    has_thumb: Union[Unset, bool] = UNSET
    id: Union[Unset, str] = UNSET
    label: Union[Unset, UpdateDatasetClipResponse200ClipLabel] = UNSET
    miss_id: Union[None, Unset, str] = UNSET
    note: Union[Unset, str] = UNSET
    origin: Union[Unset, UpdateDatasetClipResponse200ClipOrigin] = UNSET
    seconds: Union[Unset, float] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        created_at: Union[Unset, str] = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()

        event_id: Union[None, Unset, str]
        if isinstance(self.event_id, Unset):
            event_id = UNSET
        else:
            event_id = self.event_id

        has_thumb = self.has_thumb

        id = self.id

        label: Union[Unset, str] = UNSET
        if not isinstance(self.label, Unset):
            label = self.label.value

        miss_id: Union[None, Unset, str]
        if isinstance(self.miss_id, Unset):
            miss_id = UNSET
        else:
            miss_id = self.miss_id

        note = self.note

        origin: Union[Unset, str] = UNSET
        if not isinstance(self.origin, Unset):
            origin = self.origin.value

        seconds = self.seconds

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if created_at is not UNSET:
            field_dict["createdAt"] = created_at
        if event_id is not UNSET:
            field_dict["eventId"] = event_id
        if has_thumb is not UNSET:
            field_dict["hasThumb"] = has_thumb
        if id is not UNSET:
            field_dict["id"] = id
        if label is not UNSET:
            field_dict["label"] = label
        if miss_id is not UNSET:
            field_dict["missId"] = miss_id
        if note is not UNSET:
            field_dict["note"] = note
        if origin is not UNSET:
            field_dict["origin"] = origin
        if seconds is not UNSET:
            field_dict["seconds"] = seconds

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

        def _parse_event_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        event_id = _parse_event_id(d.pop("eventId", UNSET))

        has_thumb = d.pop("hasThumb", UNSET)

        id = d.pop("id", UNSET)

        _label = d.pop("label", UNSET)
        label: Union[Unset, UpdateDatasetClipResponse200ClipLabel]
        if isinstance(_label, Unset):
            label = UNSET
        else:
            label = UpdateDatasetClipResponse200ClipLabel(_label)

        def _parse_miss_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        miss_id = _parse_miss_id(d.pop("missId", UNSET))

        note = d.pop("note", UNSET)

        _origin = d.pop("origin", UNSET)
        origin: Union[Unset, UpdateDatasetClipResponse200ClipOrigin]
        if isinstance(_origin, Unset):
            origin = UNSET
        else:
            origin = UpdateDatasetClipResponse200ClipOrigin(_origin)

        seconds = d.pop("seconds", UNSET)

        update_dataset_clip_response_200_clip = cls(
            created_at=created_at,
            event_id=event_id,
            has_thumb=has_thumb,
            id=id,
            label=label,
            miss_id=miss_id,
            note=note,
            origin=origin,
            seconds=seconds,
        )

        update_dataset_clip_response_200_clip.additional_properties = d
        return update_dataset_clip_response_200_clip

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
