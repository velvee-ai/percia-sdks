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
    from ..models.list_provider_keys_response_200_keys_item import (
        ListProviderKeysResponse200KeysItem,
    )


T = TypeVar("T", bound="ListProviderKeysResponse200")


@_attrs_define
class ListProviderKeysResponse200:
    """
    Attributes:
        keys (Union[Unset, list['ListProviderKeysResponse200KeysItem']]):
    """

    keys: Union[Unset, list["ListProviderKeysResponse200KeysItem"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        keys: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.keys, Unset):
            keys = []
            for keys_item_data in self.keys:
                keys_item = keys_item_data.to_dict()
                keys.append(keys_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if keys is not UNSET:
            field_dict["keys"] = keys

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.list_provider_keys_response_200_keys_item import (
            ListProviderKeysResponse200KeysItem,
        )

        d = dict(src_dict)
        keys = []
        _keys = d.pop("keys", UNSET)
        for keys_item_data in _keys or []:
            keys_item = ListProviderKeysResponse200KeysItem.from_dict(keys_item_data)

            keys.append(keys_item)

        list_provider_keys_response_200 = cls(
            keys=keys,
        )

        list_provider_keys_response_200.additional_properties = d
        return list_provider_keys_response_200

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
