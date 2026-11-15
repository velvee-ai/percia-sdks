from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="RotateCameraTokenResponse200")


@_attrs_define
class RotateCameraTokenResponse200:
    """
    Attributes:
        expires_at (Union[Unset, None]):
        token (Union[Unset, str]):
        whip_url (Union[Unset, str]):
    """

    expires_at: Union[Unset, None] = UNSET
    token: Union[Unset, str] = UNSET
    whip_url: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        expires_at = self.expires_at

        token = self.token

        whip_url = self.whip_url

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if expires_at is not UNSET:
            field_dict["expiresAt"] = expires_at
        if token is not UNSET:
            field_dict["token"] = token
        if whip_url is not UNSET:
            field_dict["whipUrl"] = whip_url

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        expires_at = d.pop("expiresAt", UNSET)

        token = d.pop("token", UNSET)

        whip_url = d.pop("whipUrl", UNSET)

        rotate_camera_token_response_200 = cls(
            expires_at=expires_at,
            token=token,
            whip_url=whip_url,
        )

        rotate_camera_token_response_200.additional_properties = d
        return rotate_camera_token_response_200

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
