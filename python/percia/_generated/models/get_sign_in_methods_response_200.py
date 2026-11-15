from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.get_sign_in_methods_response_200_providers_item import (
        GetSignInMethodsResponse200ProvidersItem,
    )


T = TypeVar("T", bound="GetSignInMethodsResponse200")


@_attrs_define
class GetSignInMethodsResponse200:
    """
    Attributes:
        email (Union[Unset, str]):
        email_verified (Union[Unset, bool]):
        password (Union[Unset, bool]):
        providers (Union[Unset, list['GetSignInMethodsResponse200ProvidersItem']]):
    """

    email: Union[Unset, str] = UNSET
    email_verified: Union[Unset, bool] = UNSET
    password: Union[Unset, bool] = UNSET
    providers: Union[Unset, list["GetSignInMethodsResponse200ProvidersItem"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        email = self.email

        email_verified = self.email_verified

        password = self.password

        providers: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.providers, Unset):
            providers = []
            for providers_item_data in self.providers:
                providers_item = providers_item_data.to_dict()
                providers.append(providers_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if email is not UNSET:
            field_dict["email"] = email
        if email_verified is not UNSET:
            field_dict["emailVerified"] = email_verified
        if password is not UNSET:
            field_dict["password"] = password
        if providers is not UNSET:
            field_dict["providers"] = providers

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.get_sign_in_methods_response_200_providers_item import (
            GetSignInMethodsResponse200ProvidersItem,
        )

        d = dict(src_dict)
        email = d.pop("email", UNSET)

        email_verified = d.pop("emailVerified", UNSET)

        password = d.pop("password", UNSET)

        providers = []
        _providers = d.pop("providers", UNSET)
        for providers_item_data in _providers or []:
            providers_item = GetSignInMethodsResponse200ProvidersItem.from_dict(providers_item_data)

            providers.append(providers_item)

        get_sign_in_methods_response_200 = cls(
            email=email,
            email_verified=email_verified,
            password=password,
            providers=providers,
        )

        get_sign_in_methods_response_200.additional_properties = d
        return get_sign_in_methods_response_200

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
