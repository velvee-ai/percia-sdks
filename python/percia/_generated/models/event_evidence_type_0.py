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

from ..types import UNSET, Unset

T = TypeVar("T", bound="EventEvidenceType0")


@_attrs_define
class EventEvidenceType0:
    """Which wall-clock moments the stored keyframe and clip cover, so a viewer can line a clip up with the event. Null
    when neither was cut.

        Attributes:
            clip_from (Union[None, Unset, datetime.datetime]):
            clip_to (Union[None, Unset, datetime.datetime]):
            keyframe_at (Union[None, Unset, datetime.datetime]):
    """

    clip_from: Union[None, Unset, datetime.datetime] = UNSET
    clip_to: Union[None, Unset, datetime.datetime] = UNSET
    keyframe_at: Union[None, Unset, datetime.datetime] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        clip_from: Union[None, Unset, str]
        if isinstance(self.clip_from, Unset):
            clip_from = UNSET
        elif isinstance(self.clip_from, datetime.datetime):
            clip_from = self.clip_from.isoformat()
        else:
            clip_from = self.clip_from

        clip_to: Union[None, Unset, str]
        if isinstance(self.clip_to, Unset):
            clip_to = UNSET
        elif isinstance(self.clip_to, datetime.datetime):
            clip_to = self.clip_to.isoformat()
        else:
            clip_to = self.clip_to

        keyframe_at: Union[None, Unset, str]
        if isinstance(self.keyframe_at, Unset):
            keyframe_at = UNSET
        elif isinstance(self.keyframe_at, datetime.datetime):
            keyframe_at = self.keyframe_at.isoformat()
        else:
            keyframe_at = self.keyframe_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if clip_from is not UNSET:
            field_dict["clipFrom"] = clip_from
        if clip_to is not UNSET:
            field_dict["clipTo"] = clip_to
        if keyframe_at is not UNSET:
            field_dict["keyframeAt"] = keyframe_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_clip_from(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                clip_from_type_0 = isoparse(data)

                return clip_from_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        clip_from = _parse_clip_from(d.pop("clipFrom", UNSET))

        def _parse_clip_to(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                clip_to_type_0 = isoparse(data)

                return clip_to_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        clip_to = _parse_clip_to(d.pop("clipTo", UNSET))

        def _parse_keyframe_at(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                keyframe_at_type_0 = isoparse(data)

                return keyframe_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        keyframe_at = _parse_keyframe_at(d.pop("keyframeAt", UNSET))

        event_evidence_type_0 = cls(
            clip_from=clip_from,
            clip_to=clip_to,
            keyframe_at=keyframe_at,
        )

        event_evidence_type_0.additional_properties = d
        return event_evidence_type_0

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
