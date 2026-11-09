from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="GetConfigResponse200")


@_attrs_define
class GetConfigResponse200:
    """
    Attributes:
        integrations_enabled (Union[Unset, bool]): False while integrations are switched off (their routes then answer
            404).
        mail_enabled (Union[Unset, bool]):
        phone_camera_enabled (Union[Unset, bool]): False while phone cameras are switched off.
        turnstile_site_key (Union[Unset, str]):
    """

    integrations_enabled: Union[Unset, bool] = UNSET
    mail_enabled: Union[Unset, bool] = UNSET
    phone_camera_enabled: Union[Unset, bool] = UNSET
    turnstile_site_key: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        integrations_enabled = self.integrations_enabled

        mail_enabled = self.mail_enabled

        phone_camera_enabled = self.phone_camera_enabled

        turnstile_site_key = self.turnstile_site_key

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if integrations_enabled is not UNSET:
            field_dict["integrationsEnabled"] = integrations_enabled
        if mail_enabled is not UNSET:
            field_dict["mailEnabled"] = mail_enabled
        if phone_camera_enabled is not UNSET:
            field_dict["phoneCameraEnabled"] = phone_camera_enabled
        if turnstile_site_key is not UNSET:
            field_dict["turnstileSiteKey"] = turnstile_site_key

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        integrations_enabled = d.pop("integrationsEnabled", UNSET)

        mail_enabled = d.pop("mailEnabled", UNSET)

        phone_camera_enabled = d.pop("phoneCameraEnabled", UNSET)

        turnstile_site_key = d.pop("turnstileSiteKey", UNSET)

        get_config_response_200 = cls(
            integrations_enabled=integrations_enabled,
            mail_enabled=mail_enabled,
            phone_camera_enabled=phone_camera_enabled,
            turnstile_site_key=turnstile_site_key,
        )

        get_config_response_200.additional_properties = d
        return get_config_response_200

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
