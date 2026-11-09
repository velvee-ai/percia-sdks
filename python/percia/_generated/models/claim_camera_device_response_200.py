from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ClaimCameraDeviceResponse200")


@_attrs_define
class ClaimCameraDeviceResponse200:
    """
    Attributes:
        camera_id (Union[Unset, str]):
        name (Union[Unset, str]):
        token (Union[Unset, str]):
        whip_url (Union[Unset, str]):
    """

    camera_id: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    token: Union[Unset, str] = UNSET
    whip_url: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        camera_id = self.camera_id

        name = self.name

        token = self.token

        whip_url = self.whip_url

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if camera_id is not UNSET:
            field_dict["cameraId"] = camera_id
        if name is not UNSET:
            field_dict["name"] = name
        if token is not UNSET:
            field_dict["token"] = token
        if whip_url is not UNSET:
            field_dict["whipUrl"] = whip_url

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        camera_id = d.pop("cameraId", UNSET)

        name = d.pop("name", UNSET)

        token = d.pop("token", UNSET)

        whip_url = d.pop("whipUrl", UNSET)

        claim_camera_device_response_200 = cls(
            camera_id=camera_id,
            name=name,
            token=token,
            whip_url=whip_url,
        )

        claim_camera_device_response_200.additional_properties = d
        return claim_camera_device_response_200

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
