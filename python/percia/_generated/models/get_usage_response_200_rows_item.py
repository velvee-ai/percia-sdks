from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="GetUsageResponse200RowsItem")


@_attrs_define
class GetUsageResponse200RowsItem:
    """
    Attributes:
        action_calls (Union[Unset, int]):
        ai_calls (Union[Unset, int]):
        day (Union[Unset, str]):
        events (Union[Unset, int]):
        own_key (Union[Unset, int]):
        watch_hours (Union[Unset, float]):
    """

    action_calls: Union[Unset, int] = UNSET
    ai_calls: Union[Unset, int] = UNSET
    day: Union[Unset, str] = UNSET
    events: Union[Unset, int] = UNSET
    own_key: Union[Unset, int] = UNSET
    watch_hours: Union[Unset, float] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        action_calls = self.action_calls

        ai_calls = self.ai_calls

        day = self.day

        events = self.events

        own_key = self.own_key

        watch_hours = self.watch_hours

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if action_calls is not UNSET:
            field_dict["actionCalls"] = action_calls
        if ai_calls is not UNSET:
            field_dict["aiCalls"] = ai_calls
        if day is not UNSET:
            field_dict["day"] = day
        if events is not UNSET:
            field_dict["events"] = events
        if own_key is not UNSET:
            field_dict["ownKey"] = own_key
        if watch_hours is not UNSET:
            field_dict["watchHours"] = watch_hours

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        action_calls = d.pop("actionCalls", UNSET)

        ai_calls = d.pop("aiCalls", UNSET)

        day = d.pop("day", UNSET)

        events = d.pop("events", UNSET)

        own_key = d.pop("ownKey", UNSET)

        watch_hours = d.pop("watchHours", UNSET)

        get_usage_response_200_rows_item = cls(
            action_calls=action_calls,
            ai_calls=ai_calls,
            day=day,
            events=events,
            own_key=own_key,
            watch_hours=watch_hours,
        )

        get_usage_response_200_rows_item.additional_properties = d
        return get_usage_response_200_rows_item

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
