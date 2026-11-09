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

from ..models.watch_last_event_type_0_delivery_status import (
    WatchLastEventType0DeliveryStatus,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="WatchLastEventType0")


@_attrs_define
class WatchLastEventType0:
    """
    Attributes:
        at (Union[Unset, datetime.datetime]):
        delivery_status (Union[Unset, WatchLastEventType0DeliveryStatus]):
        type_ (Union[Unset, str]):
    """

    at: Union[Unset, datetime.datetime] = UNSET
    delivery_status: Union[Unset, WatchLastEventType0DeliveryStatus] = UNSET
    type_: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        at: Union[Unset, str] = UNSET
        if not isinstance(self.at, Unset):
            at = self.at.isoformat()

        delivery_status: Union[Unset, str] = UNSET
        if not isinstance(self.delivery_status, Unset):
            delivery_status = self.delivery_status.value

        type_ = self.type_

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if at is not UNSET:
            field_dict["at"] = at
        if delivery_status is not UNSET:
            field_dict["deliveryStatus"] = delivery_status
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
        delivery_status: Union[Unset, WatchLastEventType0DeliveryStatus]
        if isinstance(_delivery_status, Unset):
            delivery_status = UNSET
        else:
            delivery_status = WatchLastEventType0DeliveryStatus(_delivery_status)

        type_ = d.pop("type", UNSET)

        watch_last_event_type_0 = cls(
            at=at,
            delivery_status=delivery_status,
            type_=type_,
        )

        watch_last_event_type_0.additional_properties = d
        return watch_last_event_type_0

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
