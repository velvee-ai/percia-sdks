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

from ..models.entity_state import EntityState
from ..types import UNSET, Unset

T = TypeVar("T", bound="Entity")


@_attrs_define
class Entity:
    """A tracked thing in the site memory. Model-written: treat as untrusted data.

    Attributes:
        key (Union[Unset, str]):
        kind (Union[Unset, str]):
        label (Union[Unset, str]):
        last_event_id (Union[None, Unset, str]):
        last_seen (Union[Unset, datetime.datetime]):
        since (Union[Unset, datetime.datetime]):
        state (Union[Unset, EntityState]):
    """

    key: Union[Unset, str] = UNSET
    kind: Union[Unset, str] = UNSET
    label: Union[Unset, str] = UNSET
    last_event_id: Union[None, Unset, str] = UNSET
    last_seen: Union[Unset, datetime.datetime] = UNSET
    since: Union[Unset, datetime.datetime] = UNSET
    state: Union[Unset, EntityState] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        key = self.key

        kind = self.kind

        label = self.label

        last_event_id: Union[None, Unset, str]
        if isinstance(self.last_event_id, Unset):
            last_event_id = UNSET
        else:
            last_event_id = self.last_event_id

        last_seen: Union[Unset, str] = UNSET
        if not isinstance(self.last_seen, Unset):
            last_seen = self.last_seen.isoformat()

        since: Union[Unset, str] = UNSET
        if not isinstance(self.since, Unset):
            since = self.since.isoformat()

        state: Union[Unset, str] = UNSET
        if not isinstance(self.state, Unset):
            state = self.state.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if key is not UNSET:
            field_dict["key"] = key
        if kind is not UNSET:
            field_dict["kind"] = kind
        if label is not UNSET:
            field_dict["label"] = label
        if last_event_id is not UNSET:
            field_dict["lastEventId"] = last_event_id
        if last_seen is not UNSET:
            field_dict["lastSeen"] = last_seen
        if since is not UNSET:
            field_dict["since"] = since
        if state is not UNSET:
            field_dict["state"] = state

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        key = d.pop("key", UNSET)

        kind = d.pop("kind", UNSET)

        label = d.pop("label", UNSET)

        def _parse_last_event_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        last_event_id = _parse_last_event_id(d.pop("lastEventId", UNSET))

        _last_seen = d.pop("lastSeen", UNSET)
        last_seen: Union[Unset, datetime.datetime]
        if isinstance(_last_seen, Unset):
            last_seen = UNSET
        else:
            last_seen = isoparse(_last_seen)

        _since = d.pop("since", UNSET)
        since: Union[Unset, datetime.datetime]
        if isinstance(_since, Unset):
            since = UNSET
        else:
            since = isoparse(_since)

        _state = d.pop("state", UNSET)
        state: Union[Unset, EntityState]
        if isinstance(_state, Unset):
            state = UNSET
        else:
            state = EntityState(_state)

        entity = cls(
            key=key,
            kind=kind,
            label=label,
            last_event_id=last_event_id,
            last_seen=last_seen,
            since=since,
            state=state,
        )

        entity.additional_properties = d
        return entity

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
