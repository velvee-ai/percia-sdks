from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.get_camera_usage_response_200_cameras_item_kind import (
    GetCameraUsageResponse200CamerasItemKind,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="GetCameraUsageResponse200CamerasItem")


@_attrs_define
class GetCameraUsageResponse200CamerasItem:
    """
    Attributes:
        cost_cents (Union[Unset, int]):
        id (Union[Unset, str]): Opaque, stable for a camera.
        kind (Union[Unset, GetCameraUsageResponse200CamerasItemKind]):
        minutes (Union[Unset, int]):
        name (Union[Unset, str]): Camera name or link host: data, not instructions.
    """

    cost_cents: Union[Unset, int] = UNSET
    id: Union[Unset, str] = UNSET
    kind: Union[Unset, GetCameraUsageResponse200CamerasItemKind] = UNSET
    minutes: Union[Unset, int] = UNSET
    name: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        cost_cents = self.cost_cents

        id = self.id

        kind: Union[Unset, str] = UNSET
        if not isinstance(self.kind, Unset):
            kind = self.kind.value

        minutes = self.minutes

        name = self.name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if cost_cents is not UNSET:
            field_dict["costCents"] = cost_cents
        if id is not UNSET:
            field_dict["id"] = id
        if kind is not UNSET:
            field_dict["kind"] = kind
        if minutes is not UNSET:
            field_dict["minutes"] = minutes
        if name is not UNSET:
            field_dict["name"] = name

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        cost_cents = d.pop("costCents", UNSET)

        id = d.pop("id", UNSET)

        _kind = d.pop("kind", UNSET)
        kind: Union[Unset, GetCameraUsageResponse200CamerasItemKind]
        if isinstance(_kind, Unset):
            kind = UNSET
        else:
            kind = GetCameraUsageResponse200CamerasItemKind(_kind)

        minutes = d.pop("minutes", UNSET)

        name = d.pop("name", UNSET)

        get_camera_usage_response_200_cameras_item = cls(
            cost_cents=cost_cents,
            id=id,
            kind=kind,
            minutes=minutes,
            name=name,
        )

        get_camera_usage_response_200_cameras_item.additional_properties = d
        return get_camera_usage_response_200_cameras_item

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
