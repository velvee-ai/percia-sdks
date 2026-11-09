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

from ..models.list_devices_response_200_item_platform import (
    ListDevicesResponse200ItemPlatform,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="ListDevicesResponse200Item")


@_attrs_define
class ListDevicesResponse200Item:
    """
    Attributes:
        app_version (Union[Unset, str]):
        created_at (Union[Unset, datetime.datetime]):
        id (Union[Unset, str]):
        last_seen_at (Union[Unset, datetime.datetime]):
        platform (Union[Unset, ListDevicesResponse200ItemPlatform]):
    """

    app_version: Union[Unset, str] = UNSET
    created_at: Union[Unset, datetime.datetime] = UNSET
    id: Union[Unset, str] = UNSET
    last_seen_at: Union[Unset, datetime.datetime] = UNSET
    platform: Union[Unset, ListDevicesResponse200ItemPlatform] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        app_version = self.app_version

        created_at: Union[Unset, str] = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()

        id = self.id

        last_seen_at: Union[Unset, str] = UNSET
        if not isinstance(self.last_seen_at, Unset):
            last_seen_at = self.last_seen_at.isoformat()

        platform: Union[Unset, str] = UNSET
        if not isinstance(self.platform, Unset):
            platform = self.platform.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if app_version is not UNSET:
            field_dict["appVersion"] = app_version
        if created_at is not UNSET:
            field_dict["createdAt"] = created_at
        if id is not UNSET:
            field_dict["id"] = id
        if last_seen_at is not UNSET:
            field_dict["lastSeenAt"] = last_seen_at
        if platform is not UNSET:
            field_dict["platform"] = platform

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        app_version = d.pop("appVersion", UNSET)

        _created_at = d.pop("createdAt", UNSET)
        created_at: Union[Unset, datetime.datetime]
        if isinstance(_created_at, Unset):
            created_at = UNSET
        else:
            created_at = isoparse(_created_at)

        id = d.pop("id", UNSET)

        _last_seen_at = d.pop("lastSeenAt", UNSET)
        last_seen_at: Union[Unset, datetime.datetime]
        if isinstance(_last_seen_at, Unset):
            last_seen_at = UNSET
        else:
            last_seen_at = isoparse(_last_seen_at)

        _platform = d.pop("platform", UNSET)
        platform: Union[Unset, ListDevicesResponse200ItemPlatform]
        if isinstance(_platform, Unset):
            platform = UNSET
        else:
            platform = ListDevicesResponse200ItemPlatform(_platform)

        list_devices_response_200_item = cls(
            app_version=app_version,
            created_at=created_at,
            id=id,
            last_seen_at=last_seen_at,
            platform=platform,
        )

        list_devices_response_200_item.additional_properties = d
        return list_devices_response_200_item

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
