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

from ..models.get_sign_in_methods_response_200_providers_item_provider import (
    GetSignInMethodsResponse200ProvidersItemProvider,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="GetSignInMethodsResponse200ProvidersItem")


@_attrs_define
class GetSignInMethodsResponse200ProvidersItem:
    """
    Attributes:
        linked_at (Union[None, Unset, datetime.datetime]):
        provider (Union[Unset, GetSignInMethodsResponse200ProvidersItemProvider]):
    """

    linked_at: Union[None, Unset, datetime.datetime] = UNSET
    provider: Union[Unset, GetSignInMethodsResponse200ProvidersItemProvider] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        linked_at: Union[None, Unset, str]
        if isinstance(self.linked_at, Unset):
            linked_at = UNSET
        elif isinstance(self.linked_at, datetime.datetime):
            linked_at = self.linked_at.isoformat()
        else:
            linked_at = self.linked_at

        provider: Union[Unset, str] = UNSET
        if not isinstance(self.provider, Unset):
            provider = self.provider.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if linked_at is not UNSET:
            field_dict["linkedAt"] = linked_at
        if provider is not UNSET:
            field_dict["provider"] = provider

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_linked_at(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                linked_at_type_0 = isoparse(data)

                return linked_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        linked_at = _parse_linked_at(d.pop("linkedAt", UNSET))

        _provider = d.pop("provider", UNSET)
        provider: Union[Unset, GetSignInMethodsResponse200ProvidersItemProvider]
        if isinstance(_provider, Unset):
            provider = UNSET
        else:
            provider = GetSignInMethodsResponse200ProvidersItemProvider(_provider)

        get_sign_in_methods_response_200_providers_item = cls(
            linked_at=linked_at,
            provider=provider,
        )

        get_sign_in_methods_response_200_providers_item.additional_properties = d
        return get_sign_in_methods_response_200_providers_item

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
