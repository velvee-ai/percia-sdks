from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.create_api_key_response_201_scopes_item import (
    CreateApiKeyResponse201ScopesItem,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateApiKeyResponse201")


@_attrs_define
class CreateApiKeyResponse201:
    """
    Attributes:
        id (Union[Unset, str]):
        key (Union[Unset, str]):
        name (Union[Unset, str]):
        prefix (Union[Unset, str]):
        scopes (Union[Unset, list[CreateApiKeyResponse201ScopesItem]]):
    """

    id: Union[Unset, str] = UNSET
    key: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    prefix: Union[Unset, str] = UNSET
    scopes: Union[Unset, list[CreateApiKeyResponse201ScopesItem]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        key = self.key

        name = self.name

        prefix = self.prefix

        scopes: Union[Unset, list[str]] = UNSET
        if not isinstance(self.scopes, Unset):
            scopes = []
            for scopes_item_data in self.scopes:
                scopes_item = scopes_item_data.value
                scopes.append(scopes_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if key is not UNSET:
            field_dict["key"] = key
        if name is not UNSET:
            field_dict["name"] = name
        if prefix is not UNSET:
            field_dict["prefix"] = prefix
        if scopes is not UNSET:
            field_dict["scopes"] = scopes

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id", UNSET)

        key = d.pop("key", UNSET)

        name = d.pop("name", UNSET)

        prefix = d.pop("prefix", UNSET)

        scopes = []
        _scopes = d.pop("scopes", UNSET)
        for scopes_item_data in _scopes or []:
            scopes_item = CreateApiKeyResponse201ScopesItem(scopes_item_data)

            scopes.append(scopes_item)

        create_api_key_response_201 = cls(
            id=id,
            key=key,
            name=name,
            prefix=prefix,
            scopes=scopes,
        )

        create_api_key_response_201.additional_properties = d
        return create_api_key_response_201

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
