from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
    Union,
    cast,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.get_site_timeline_response_200_events_item import (
        GetSiteTimelineResponse200EventsItem,
    )


T = TypeVar("T", bound="GetSiteTimelineResponse200")


@_attrs_define
class GetSiteTimelineResponse200:
    """
    Attributes:
        events (Union[Unset, list['GetSiteTimelineResponse200EventsItem']]):
        next_cursor (Union[None, Unset, str]):
    """

    events: Union[Unset, list["GetSiteTimelineResponse200EventsItem"]] = UNSET
    next_cursor: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        events: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.events, Unset):
            events = []
            for events_item_data in self.events:
                events_item = events_item_data.to_dict()
                events.append(events_item)

        next_cursor: Union[None, Unset, str]
        if isinstance(self.next_cursor, Unset):
            next_cursor = UNSET
        else:
            next_cursor = self.next_cursor

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if events is not UNSET:
            field_dict["events"] = events
        if next_cursor is not UNSET:
            field_dict["nextCursor"] = next_cursor

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.get_site_timeline_response_200_events_item import (
            GetSiteTimelineResponse200EventsItem,
        )

        d = dict(src_dict)
        events = []
        _events = d.pop("events", UNSET)
        for events_item_data in _events or []:
            events_item = GetSiteTimelineResponse200EventsItem.from_dict(events_item_data)

            events.append(events_item)

        def _parse_next_cursor(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        next_cursor = _parse_next_cursor(d.pop("nextCursor", UNSET))

        get_site_timeline_response_200 = cls(
            events=events,
            next_cursor=next_cursor,
        )

        get_site_timeline_response_200.additional_properties = d
        return get_site_timeline_response_200

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
