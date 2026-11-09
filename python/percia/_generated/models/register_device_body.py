from collections.abc import Mapping
from typing import (
    Any,
    Literal,
    TypeVar,
    cast,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="RegisterDeviceBody")


@_attrs_define
class RegisterDeviceBody:
    """
    Attributes:
        app_version (str):
        platform (Literal['ios']):
        token (str):
    """

    app_version: str
    platform: Literal["ios"]
    token: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        app_version = self.app_version

        platform = self.platform

        token = self.token

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "appVersion": app_version,
                "platform": platform,
                "token": token,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        app_version = d.pop("appVersion")

        platform = cast(Literal["ios"], d.pop("platform"))
        if platform != "ios":
            raise ValueError(f"platform must match const 'ios', got '{platform}'")

        token = d.pop("token")

        register_device_body = cls(
            app_version=app_version,
            platform=platform,
            token=token,
        )

        register_device_body.additional_properties = d
        return register_device_body

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
