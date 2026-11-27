import datetime
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
from dateutil.parser import isoparse

from ..models.camera_device_kind_type_1 import CameraDeviceKindType1
from ..models.camera_kind import CameraKind
from ..models.camera_status import CameraStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.camera_pull import CameraPull


T = TypeVar("T", bound="Camera")


@_attrs_define
class Camera:
    """
    Attributes:
        device_kind (Union[CameraDeviceKindType1, None, Unset]): What device a paired camera is, when the browser that
            made it said so; null for older cameras and for push cameras. Wording only.
        external_id (Union[None, Unset, str]): The connector's own id for a push camera.
        id (Union[Unset, str]):
        kind (Union[Unset, CameraKind]): phone = paired by link; push = a connector on a LAN pushes WHIP with a token;
            link = a public RTSP/RTSPS/HTTP/HTTPS address Percia pulls itself; file = an uploaded video, played once. link
            and file exist while PULL_CAMERAS is on.
        last_seen_at (Union[None, Unset, datetime.datetime]):
        name (Union[Unset, str]):
        pull (Union[Unset, CameraPull]): link and file cameras only: the last report of the puller. Never an address.
        status (Union[Unset, CameraStatus]): online = heartbeat or an allowed publish under 60 s ago.
        watch_count (Union[Unset, int]):
    """

    device_kind: Union[CameraDeviceKindType1, None, Unset] = UNSET
    external_id: Union[None, Unset, str] = UNSET
    id: Union[Unset, str] = UNSET
    kind: Union[Unset, CameraKind] = UNSET
    last_seen_at: Union[None, Unset, datetime.datetime] = UNSET
    name: Union[Unset, str] = UNSET
    pull: Union[Unset, "CameraPull"] = UNSET
    status: Union[Unset, CameraStatus] = UNSET
    watch_count: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        device_kind: Union[None, Unset, str]
        if isinstance(self.device_kind, Unset):
            device_kind = UNSET
        elif isinstance(self.device_kind, CameraDeviceKindType1):
            device_kind = self.device_kind.value
        else:
            device_kind = self.device_kind

        external_id: Union[None, Unset, str]
        if isinstance(self.external_id, Unset):
            external_id = UNSET
        else:
            external_id = self.external_id

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

        name = self.name

        pull: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.pull, Unset):
            pull = self.pull.to_dict()

        status: Union[Unset, str] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        watch_count = self.watch_count

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if device_kind is not UNSET:
            field_dict["deviceKind"] = device_kind
        if external_id is not UNSET:
            field_dict["externalId"] = external_id
        if id is not UNSET:
            field_dict["id"] = id
        if kind is not UNSET:
            field_dict["kind"] = kind
        if last_seen_at is not UNSET:
            field_dict["lastSeenAt"] = last_seen_at
        if name is not UNSET:
            field_dict["name"] = name
        if pull is not UNSET:
            field_dict["pull"] = pull
        if status is not UNSET:
            field_dict["status"] = status
        if watch_count is not UNSET:
            field_dict["watchCount"] = watch_count

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.camera_pull import CameraPull

        d = dict(src_dict)

        def _parse_device_kind(
            data: object,
        ) -> Union[CameraDeviceKindType1, None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                device_kind_type_1 = CameraDeviceKindType1(data)

                return device_kind_type_1
            except:  # noqa: E722
                pass
            return cast(Union[CameraDeviceKindType1, None, Unset], data)

        device_kind = _parse_device_kind(d.pop("deviceKind", UNSET))

        def _parse_external_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        external_id = _parse_external_id(d.pop("externalId", UNSET))

        id = d.pop("id", UNSET)

        _kind = d.pop("kind", UNSET)
        kind: Union[Unset, CameraKind]
        if isinstance(_kind, Unset):
            kind = UNSET
        else:
            kind = CameraKind(_kind)

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

        name = d.pop("name", UNSET)

        _pull = d.pop("pull", UNSET)
        pull: Union[Unset, CameraPull]
        if isinstance(_pull, Unset):
            pull = UNSET
        else:
            pull = CameraPull.from_dict(_pull)

        _status = d.pop("status", UNSET)
        status: Union[Unset, CameraStatus]
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = CameraStatus(_status)

        watch_count = d.pop("watchCount", UNSET)

        camera = cls(
            device_kind=device_kind,
            external_id=external_id,
            id=id,
            kind=kind,
            last_seen_at=last_seen_at,
            name=name,
            pull=pull,
            status=status,
            watch_count=watch_count,
        )

        camera.additional_properties = d
        return camera

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
