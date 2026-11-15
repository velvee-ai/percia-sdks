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

from ..models.get_camera_status_response_200_kind import GetCameraStatusResponse200Kind
from ..models.get_camera_status_response_200_state import (
    GetCameraStatusResponse200State,
)
from ..models.get_camera_status_response_200_status import (
    GetCameraStatusResponse200Status,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="GetCameraStatusResponse200")


@_attrs_define
class GetCameraStatusResponse200:
    """
    Attributes:
        hint (Union[None, Unset, str]):
        id (Union[Unset, str]):
        kind (Union[Unset, GetCameraStatusResponse200Kind]):
        last_seen_at (Union[None, Unset, datetime.datetime]):
        seconds_since_seen (Union[None, Unset, int]):
        state (Union[Unset, GetCameraStatusResponse200State]):
        status (Union[Unset, GetCameraStatusResponse200Status]):
        watch_count (Union[Unset, int]):
    """

    hint: Union[None, Unset, str] = UNSET
    id: Union[Unset, str] = UNSET
    kind: Union[Unset, GetCameraStatusResponse200Kind] = UNSET
    last_seen_at: Union[None, Unset, datetime.datetime] = UNSET
    seconds_since_seen: Union[None, Unset, int] = UNSET
    state: Union[Unset, GetCameraStatusResponse200State] = UNSET
    status: Union[Unset, GetCameraStatusResponse200Status] = UNSET
    watch_count: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        hint: Union[None, Unset, str]
        if isinstance(self.hint, Unset):
            hint = UNSET
        else:
            hint = self.hint

        id = self.id

        kind: Union[Unset, str] = UNSET
        if not isinstance(self.kind, Unset):
            kind = self.kind.value

        last_seen_at: Union[None, Unset, str]
        if isinstance(self.last_seen_at, Unset):
            last_seen_at = UNSET
        elif isinstance(self.last_seen_at, datetime.datetime):
            last_seen_at = self.last_seen_at.isoformat()
        else:
            last_seen_at = self.last_seen_at

        seconds_since_seen: Union[None, Unset, int]
        if isinstance(self.seconds_since_seen, Unset):
            seconds_since_seen = UNSET
        else:
            seconds_since_seen = self.seconds_since_seen

        state: Union[Unset, str] = UNSET
        if not isinstance(self.state, Unset):
            state = self.state.value

        status: Union[Unset, str] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        watch_count = self.watch_count

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if hint is not UNSET:
            field_dict["hint"] = hint
        if id is not UNSET:
            field_dict["id"] = id
        if kind is not UNSET:
            field_dict["kind"] = kind
        if last_seen_at is not UNSET:
            field_dict["lastSeenAt"] = last_seen_at
        if seconds_since_seen is not UNSET:
            field_dict["secondsSinceSeen"] = seconds_since_seen
        if state is not UNSET:
            field_dict["state"] = state
        if status is not UNSET:
            field_dict["status"] = status
        if watch_count is not UNSET:
            field_dict["watchCount"] = watch_count

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_hint(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        hint = _parse_hint(d.pop("hint", UNSET))

        id = d.pop("id", UNSET)

        _kind = d.pop("kind", UNSET)
        kind: Union[Unset, GetCameraStatusResponse200Kind]
        if isinstance(_kind, Unset):
            kind = UNSET
        else:
            kind = GetCameraStatusResponse200Kind(_kind)

        def _parse_last_seen_at(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                last_seen_at_type_0 = isoparse(data)

                return last_seen_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        last_seen_at = _parse_last_seen_at(d.pop("lastSeenAt", UNSET))

        def _parse_seconds_since_seen(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        seconds_since_seen = _parse_seconds_since_seen(d.pop("secondsSinceSeen", UNSET))

        _state = d.pop("state", UNSET)
        state: Union[Unset, GetCameraStatusResponse200State]
        if isinstance(_state, Unset):
            state = UNSET
        else:
            state = GetCameraStatusResponse200State(_state)

        _status = d.pop("status", UNSET)
        status: Union[Unset, GetCameraStatusResponse200Status]
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = GetCameraStatusResponse200Status(_status)

        watch_count = d.pop("watchCount", UNSET)

        get_camera_status_response_200 = cls(
            hint=hint,
            id=id,
            kind=kind,
            last_seen_at=last_seen_at,
            seconds_since_seen=seconds_since_seen,
            state=state,
            status=status,
            watch_count=watch_count,
        )

        get_camera_status_response_200.additional_properties = d
        return get_camera_status_response_200

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
