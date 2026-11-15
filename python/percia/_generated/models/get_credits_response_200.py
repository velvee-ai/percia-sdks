from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
    Union,
    cast,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.get_credits_response_200_grants_item import (
        GetCreditsResponse200GrantsItem,
    )
    from ..models.get_credits_response_200_redemptions_item import (
        GetCreditsResponse200RedemptionsItem,
    )


T = TypeVar("T", bound="GetCreditsResponse200")


@_attrs_define
class GetCreditsResponse200:
    """
    Attributes:
        credit_expires_at (Union[None, Unset, str]):
        credit_minutes (Union[Unset, int]):
        grants (Union[Unset, list['GetCreditsResponse200GrantsItem']]):
        redemptions (Union[Unset, list['GetCreditsResponse200RedemptionsItem']]):
    """

    credit_expires_at: Union[None, Unset, str] = UNSET
    credit_minutes: Union[Unset, int] = UNSET
    grants: Union[Unset, list["GetCreditsResponse200GrantsItem"]] = UNSET
    redemptions: Union[Unset, list["GetCreditsResponse200RedemptionsItem"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        credit_expires_at: Union[None, Unset, str]
        if isinstance(self.credit_expires_at, Unset):
            credit_expires_at = UNSET
        else:
            credit_expires_at = self.credit_expires_at

        credit_minutes = self.credit_minutes

        grants: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.grants, Unset):
            grants = []
            for grants_item_data in self.grants:
                grants_item = grants_item_data.to_dict()
                grants.append(grants_item)

        redemptions: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.redemptions, Unset):
            redemptions = []
            for redemptions_item_data in self.redemptions:
                redemptions_item = redemptions_item_data.to_dict()
                redemptions.append(redemptions_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if credit_expires_at is not UNSET:
            field_dict["creditExpiresAt"] = credit_expires_at
        if credit_minutes is not UNSET:
            field_dict["creditMinutes"] = credit_minutes
        if grants is not UNSET:
            field_dict["grants"] = grants
        if redemptions is not UNSET:
            field_dict["redemptions"] = redemptions

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.get_credits_response_200_grants_item import (
            GetCreditsResponse200GrantsItem,
        )
        from ..models.get_credits_response_200_redemptions_item import (
            GetCreditsResponse200RedemptionsItem,
        )

        d = dict(src_dict)

        def _parse_credit_expires_at(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        credit_expires_at = _parse_credit_expires_at(d.pop("creditExpiresAt", UNSET))

        credit_minutes = d.pop("creditMinutes", UNSET)

        grants = []
        _grants = d.pop("grants", UNSET)
        for grants_item_data in _grants or []:
            grants_item = GetCreditsResponse200GrantsItem.from_dict(grants_item_data)

            grants.append(grants_item)

        redemptions = []
        _redemptions = d.pop("redemptions", UNSET)
        for redemptions_item_data in _redemptions or []:
            redemptions_item = GetCreditsResponse200RedemptionsItem.from_dict(redemptions_item_data)

            redemptions.append(redemptions_item)

        get_credits_response_200 = cls(
            credit_expires_at=credit_expires_at,
            credit_minutes=credit_minutes,
            grants=grants,
            redemptions=redemptions,
        )

        get_credits_response_200.additional_properties = d
        return get_credits_response_200

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
