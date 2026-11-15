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

from ..models.get_watch_response_200_last_event_type_0_delivery_status import (
    GetWatchResponse200LastEventType0DeliveryStatus,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="GetWatchResponse200LastEventType0")


@_attrs_define
class GetWatchResponse200LastEventType0:
    """
    Attributes:
        at (Union[Unset, datetime.datetime]):
        delivery_status (Union[Unset, GetWatchResponse200LastEventType0DeliveryStatus]):
        has_keyframe (Union[Unset, bool]): False when no keyframe was kept or it has passed its retention days.
        id (Union[Unset, str]): The newest event id; with hasKeyframe it addresses GET
            /watches/{id}/events/{eventId}/keyframe.
        type_ (Union[Unset, str]):
    """

    at: Union[Unset, datetime.datetime] = UNSET
    delivery_status: Union[Unset, GetWatchResponse200LastEventType0DeliveryStatus] = UNSET
    has_keyframe: Union[Unset, bool] = UNSET
    id: Union[Unset, str] = UNSET
    type_: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        at: Union[Unset, str] = UNSET
        if not isinstance(self.at, Unset):
            at = self.at.isoformat()

        delivery_status: Union[Unset, str] = UNSET
        if not isinstance(self.delivery_status, Unset):
            delivery_status = self.delivery_status.value

        has_keyframe = self.has_keyframe

        id = self.id

        type_ = self.type_

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if at is not UNSET:
            field_dict["at"] = at
        if delivery_status is not UNSET:
            field_dict["deliveryStatus"] = delivery_status
        if has_keyframe is not UNSET:
            field_dict["hasKeyframe"] = has_keyframe
        if id is not UNSET:
            field_dict["id"] = id
        if type_ is not UNSET:
            field_dict["type"] = type_

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _at = d.pop("at", UNSET)
        at: Union[Unset, datetime.datetime]
        if isinstance(_at, Unset):
            at = UNSET
        else:
            at = isoparse(_at)

        _delivery_status = d.pop("deliveryStatus", UNSET)
        delivery_status: Union[Unset, GetWatchResponse200LastEventType0DeliveryStatus]
        if isinstance(_delivery_status, Unset):
            delivery_status = UNSET
        else:
            delivery_status = GetWatchResponse200LastEventType0DeliveryStatus(_delivery_status)

        has_keyframe = d.pop("hasKeyframe", UNSET)

        id = d.pop("id", UNSET)

        type_ = d.pop("type", UNSET)

        get_watch_response_200_last_event_type_0 = cls(
            at=at,
            delivery_status=delivery_status,
            has_keyframe=has_keyframe,
            id=id,
            type_=type_,
        )

        get_watch_response_200_last_event_type_0.additional_properties = d
        return get_watch_response_200_last_event_type_0

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
