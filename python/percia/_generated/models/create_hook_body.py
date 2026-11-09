from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.create_hook_body_events_item import CreateHookBodyEventsItem
from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateHookBody")


@_attrs_define
class CreateHookBody:
    """
    Attributes:
        events (list[CreateHookBodyEventsItem]): Event types to send: `goal.met`, or `*` for all.
        url (str): https address that receives a signed POST for each event. Must be public.
        label (Union[Unset, str]): A name to recognise the hook by, such as the Zap's name.
        watch_id (Union[Unset, str]): Only events of this watch. Omit for every watch you own.
    """

    events: list[CreateHookBodyEventsItem]
    url: str
    label: Union[Unset, str] = UNSET
    watch_id: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        events = []
        for events_item_data in self.events:
            events_item = events_item_data.value
            events.append(events_item)

        url = self.url

        label = self.label

        watch_id = self.watch_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "events": events,
                "url": url,
            }
        )
        if label is not UNSET:
            field_dict["label"] = label
        if watch_id is not UNSET:
            field_dict["watchId"] = watch_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        events = []
        _events = d.pop("events")
        for events_item_data in _events:
            events_item = CreateHookBodyEventsItem(events_item_data)

            events.append(events_item)

        url = d.pop("url")

        label = d.pop("label", UNSET)

        watch_id = d.pop("watchId", UNSET)

        create_hook_body = cls(
            events=events,
            url=url,
            label=label,
            watch_id=watch_id,
        )

        create_hook_body.additional_properties = d
        return create_hook_body

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
