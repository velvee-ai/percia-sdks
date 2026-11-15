from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
    cast,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.get_credits_response_200_grants_item_source import (
    GetCreditsResponse200GrantsItemSource,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="GetCreditsResponse200GrantsItem")


@_attrs_define
class GetCreditsResponse200GrantsItem:
    """
    Attributes:
        expires_at (Union[None, Unset, str]):
        id (Union[Unset, str]):
        minutes (Union[Unset, int]):
        remaining (Union[Unset, int]):
        source (Union[Unset, GetCreditsResponse200GrantsItemSource]):
    """

    expires_at: Union[None, Unset, str] = UNSET
    id: Union[Unset, str] = UNSET
    minutes: Union[Unset, int] = UNSET
    remaining: Union[Unset, int] = UNSET
    source: Union[Unset, GetCreditsResponse200GrantsItemSource] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        expires_at: Union[None, Unset, str]
        if isinstance(self.expires_at, Unset):
            expires_at = UNSET
        else:
            expires_at = self.expires_at

        id = self.id

        minutes = self.minutes

        remaining = self.remaining

        source: Union[Unset, str] = UNSET
        if not isinstance(self.source, Unset):
            source = self.source.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if expires_at is not UNSET:
            field_dict["expiresAt"] = expires_at
        if id is not UNSET:
            field_dict["id"] = id
        if minutes is not UNSET:
            field_dict["minutes"] = minutes
        if remaining is not UNSET:
            field_dict["remaining"] = remaining
        if source is not UNSET:
            field_dict["source"] = source

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_expires_at(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        expires_at = _parse_expires_at(d.pop("expiresAt", UNSET))

        id = d.pop("id", UNSET)

        minutes = d.pop("minutes", UNSET)

        remaining = d.pop("remaining", UNSET)

        _source = d.pop("source", UNSET)
        source: Union[Unset, GetCreditsResponse200GrantsItemSource]
        if isinstance(_source, Unset):
            source = UNSET
        else:
            source = GetCreditsResponse200GrantsItemSource(_source)

        get_credits_response_200_grants_item = cls(
            expires_at=expires_at,
            id=id,
            minutes=minutes,
            remaining=remaining,
            source=source,
        )

        get_credits_response_200_grants_item.additional_properties = d
        return get_credits_response_200_grants_item

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
