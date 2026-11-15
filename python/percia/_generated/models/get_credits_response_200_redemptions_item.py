from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="GetCreditsResponse200RedemptionsItem")


@_attrs_define
class GetCreditsResponse200RedemptionsItem:
    """
    Attributes:
        minutes (Union[Unset, int]):
        redeemed_at (Union[Unset, str]):
    """

    minutes: Union[Unset, int] = UNSET
    redeemed_at: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        minutes = self.minutes

        redeemed_at = self.redeemed_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if minutes is not UNSET:
            field_dict["minutes"] = minutes
        if redeemed_at is not UNSET:
            field_dict["redeemedAt"] = redeemed_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        minutes = d.pop("minutes", UNSET)

        redeemed_at = d.pop("redeemedAt", UNSET)

        get_credits_response_200_redemptions_item = cls(
            minutes=minutes,
            redeemed_at=redeemed_at,
        )

        get_credits_response_200_redemptions_item.additional_properties = d
        return get_credits_response_200_redemptions_item

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
