from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
    cast,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="RedeemCreditCodeResponse200")


@_attrs_define
class RedeemCreditCodeResponse200:
    """
    Attributes:
        credit_minutes (Union[Unset, int]):
        expires_at (Union[None, Unset, str]):
        free_minutes_left (Union[Unset, int]):
        granted_minutes (Union[Unset, int]):
    """

    credit_minutes: Union[Unset, int] = UNSET
    expires_at: Union[None, Unset, str] = UNSET
    free_minutes_left: Union[Unset, int] = UNSET
    granted_minutes: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        credit_minutes = self.credit_minutes

        expires_at: Union[None, Unset, str]
        if isinstance(self.expires_at, Unset):
            expires_at = UNSET
        else:
            expires_at = self.expires_at

        free_minutes_left = self.free_minutes_left

        granted_minutes = self.granted_minutes

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if credit_minutes is not UNSET:
            field_dict["creditMinutes"] = credit_minutes
        if expires_at is not UNSET:
            field_dict["expiresAt"] = expires_at
        if free_minutes_left is not UNSET:
            field_dict["freeMinutesLeft"] = free_minutes_left
        if granted_minutes is not UNSET:
            field_dict["grantedMinutes"] = granted_minutes

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        credit_minutes = d.pop("creditMinutes", UNSET)

        def _parse_expires_at(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        expires_at = _parse_expires_at(d.pop("expiresAt", UNSET))

        free_minutes_left = d.pop("freeMinutesLeft", UNSET)

        granted_minutes = d.pop("grantedMinutes", UNSET)

        redeem_credit_code_response_200 = cls(
            credit_minutes=credit_minutes,
            expires_at=expires_at,
            free_minutes_left=free_minutes_left,
            granted_minutes=granted_minutes,
        )

        redeem_credit_code_response_200.additional_properties = d
        return redeem_credit_code_response_200

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
