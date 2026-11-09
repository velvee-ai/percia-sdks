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

from ..models.list_provider_keys_response_200_keys_item_provider import (
    ListProviderKeysResponse200KeysItemProvider,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="ListProviderKeysResponse200KeysItem")


@_attrs_define
class ListProviderKeysResponse200KeysItem:
    """
    Attributes:
        added_at (Union[Unset, datetime.datetime]):
        last4 (Union[Unset, str]):
        provider (Union[Unset, ListProviderKeysResponse200KeysItemProvider]):
    """

    added_at: Union[Unset, datetime.datetime] = UNSET
    last4: Union[Unset, str] = UNSET
    provider: Union[Unset, ListProviderKeysResponse200KeysItemProvider] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        added_at: Union[Unset, str] = UNSET
        if not isinstance(self.added_at, Unset):
            added_at = self.added_at.isoformat()

        last4 = self.last4

        provider: Union[Unset, str] = UNSET
        if not isinstance(self.provider, Unset):
            provider = self.provider.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if added_at is not UNSET:
            field_dict["addedAt"] = added_at
        if last4 is not UNSET:
            field_dict["last4"] = last4
        if provider is not UNSET:
            field_dict["provider"] = provider

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _added_at = d.pop("addedAt", UNSET)
        added_at: Union[Unset, datetime.datetime]
        if isinstance(_added_at, Unset):
            added_at = UNSET
        else:
            added_at = isoparse(_added_at)

        last4 = d.pop("last4", UNSET)

        _provider = d.pop("provider", UNSET)
        provider: Union[Unset, ListProviderKeysResponse200KeysItemProvider]
        if isinstance(_provider, Unset):
            provider = UNSET
        else:
            provider = ListProviderKeysResponse200KeysItemProvider(_provider)

        list_provider_keys_response_200_keys_item = cls(
            added_at=added_at,
            last4=last4,
            provider=provider,
        )

        list_provider_keys_response_200_keys_item.additional_properties = d
        return list_provider_keys_response_200_keys_item

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
