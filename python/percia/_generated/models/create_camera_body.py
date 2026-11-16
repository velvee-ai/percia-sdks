from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.create_camera_body_device_kind import CreateCameraBodyDeviceKind
from ..models.create_camera_body_kind import CreateCameraBodyKind
from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateCameraBody")


@_attrs_define
class CreateCameraBody:
    """
    Attributes:
        name (str):
        device_kind (Union[Unset, CreateCameraBodyDeviceKind]):
        external_id (Union[Unset, str]):
        kind (Union[Unset, CreateCameraBodyKind]):
    """

    name: str
    device_kind: Union[Unset, CreateCameraBodyDeviceKind] = UNSET
    external_id: Union[Unset, str] = UNSET
    kind: Union[Unset, CreateCameraBodyKind] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        device_kind: Union[Unset, str] = UNSET
        if not isinstance(self.device_kind, Unset):
            device_kind = self.device_kind.value

        external_id = self.external_id

        kind: Union[Unset, str] = UNSET
        if not isinstance(self.kind, Unset):
            kind = self.kind.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
            }
        )
        if device_kind is not UNSET:
            field_dict["deviceKind"] = device_kind
        if external_id is not UNSET:
            field_dict["externalId"] = external_id
        if kind is not UNSET:
            field_dict["kind"] = kind

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        _device_kind = d.pop("deviceKind", UNSET)
        device_kind: Union[Unset, CreateCameraBodyDeviceKind]
        if isinstance(_device_kind, Unset):
            device_kind = UNSET
        else:
            device_kind = CreateCameraBodyDeviceKind(_device_kind)

        external_id = d.pop("externalId", UNSET)

        _kind = d.pop("kind", UNSET)
        kind: Union[Unset, CreateCameraBodyKind]
        if isinstance(_kind, Unset):
            kind = UNSET
        else:
            kind = CreateCameraBodyKind(_kind)

        create_camera_body = cls(
            name=name,
            device_kind=device_kind,
            external_id=external_id,
            kind=kind,
        )

        create_camera_body.additional_properties = d
        return create_camera_body

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
