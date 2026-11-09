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

from ..models.hook_created_events_item import HookCreatedEventsItem
from ..models.hook_created_status import HookCreatedStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="HookCreated")


@_attrs_define
class HookCreated:
    """The new hook plus its signing secret, shown only here.

    Attributes:
        created_at (datetime.datetime):
        events (list[HookCreatedEventsItem]):
        id (str):
        secret (str): `whsec_...`. Verify deliveries with it (webhooks guide). Shown once.
        status (HookCreatedStatus): disabled = Percia stopped sending (the receiver answered 410, or deliveries kept
            failing). Create the hook again.
        label (Union[None, Unset, str]):
        last_delivered_at (Union[None, Unset, datetime.datetime]):
        last_error (Union[None, Unset, str]): Stable code: why it was disabled, or why the last delivery failed.
        watch_id (Union[None, Unset, str]): Null = every watch you own.
    """

    created_at: datetime.datetime
    events: list[HookCreatedEventsItem]
    id: str
    secret: str
    status: HookCreatedStatus
    label: Union[None, Unset, str] = UNSET
    last_delivered_at: Union[None, Unset, datetime.datetime] = UNSET
    last_error: Union[None, Unset, str] = UNSET
    watch_id: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        created_at = self.created_at.isoformat()

        events = []
        for events_item_data in self.events:
            events_item = events_item_data.value
            events.append(events_item)

        id = self.id

        secret = self.secret

        status = self.status.value

        label: Union[None, Unset, str]
        if isinstance(self.label, Unset):
            label = UNSET
        else:
            label = self.label

        last_delivered_at: Union[None, Unset, str]
        if isinstance(self.last_delivered_at, Unset):
            last_delivered_at = UNSET
        elif isinstance(self.last_delivered_at, datetime.datetime):
            last_delivered_at = self.last_delivered_at.isoformat()
        else:
            last_delivered_at = self.last_delivered_at

        last_error: Union[None, Unset, str]
        if isinstance(self.last_error, Unset):
            last_error = UNSET
        else:
            last_error = self.last_error

        watch_id: Union[None, Unset, str]
        if isinstance(self.watch_id, Unset):
            watch_id = UNSET
        else:
            watch_id = self.watch_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "createdAt": created_at,
                "events": events,
                "id": id,
                "secret": secret,
                "status": status,
            }
        )
        if label is not UNSET:
            field_dict["label"] = label
        if last_delivered_at is not UNSET:
            field_dict["lastDeliveredAt"] = last_delivered_at
        if last_error is not UNSET:
            field_dict["lastError"] = last_error
        if watch_id is not UNSET:
            field_dict["watchId"] = watch_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        created_at = isoparse(d.pop("createdAt"))

        events = []
        _events = d.pop("events")
        for events_item_data in _events:
            events_item = HookCreatedEventsItem(events_item_data)

            events.append(events_item)

        id = d.pop("id")

        secret = d.pop("secret")

        status = HookCreatedStatus(d.pop("status"))

        def _parse_label(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        label = _parse_label(d.pop("label", UNSET))

        def _parse_last_delivered_at(
            data: object,
        ) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                last_delivered_at_type_0 = isoparse(data)

                return last_delivered_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        last_delivered_at = _parse_last_delivered_at(d.pop("lastDeliveredAt", UNSET))

        def _parse_last_error(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        last_error = _parse_last_error(d.pop("lastError", UNSET))

        def _parse_watch_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        watch_id = _parse_watch_id(d.pop("watchId", UNSET))

        hook_created = cls(
            created_at=created_at,
            events=events,
            id=id,
            secret=secret,
            status=status,
            label=label,
            last_delivered_at=last_delivered_at,
            last_error=last_error,
            watch_id=watch_id,
        )

        hook_created.additional_properties = d
        return hook_created

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
