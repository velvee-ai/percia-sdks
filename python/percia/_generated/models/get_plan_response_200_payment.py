from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
    cast,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.get_plan_response_200_payment_state import GetPlanResponse200PaymentState
from ..types import UNSET, Unset

T = TypeVar("T", bound="GetPlanResponse200Payment")


@_attrs_define
class GetPlanResponse200Payment:
    """Failed-payment state. state: active, grace (a payment failed; everything works until graceEndsAt) or blocked (writes
    answer 402 payment_required; update the payment method on the Billing page).

        Attributes:
            billing_url (Union[Unset, str]):
            blocked_at (Union[None, Unset, str]):
            grace_ends_at (Union[None, Unset, str]):
            grace_started_at (Union[None, Unset, str]):
            state (Union[Unset, GetPlanResponse200PaymentState]):
    """

    billing_url: Union[Unset, str] = UNSET
    blocked_at: Union[None, Unset, str] = UNSET
    grace_ends_at: Union[None, Unset, str] = UNSET
    grace_started_at: Union[None, Unset, str] = UNSET
    state: Union[Unset, GetPlanResponse200PaymentState] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        billing_url = self.billing_url

        blocked_at: Union[None, Unset, str]
        if isinstance(self.blocked_at, Unset):
            blocked_at = UNSET
        else:
            blocked_at = self.blocked_at

        grace_ends_at: Union[None, Unset, str]
        if isinstance(self.grace_ends_at, Unset):
            grace_ends_at = UNSET
        else:
            grace_ends_at = self.grace_ends_at

        grace_started_at: Union[None, Unset, str]
        if isinstance(self.grace_started_at, Unset):
            grace_started_at = UNSET
        else:
            grace_started_at = self.grace_started_at

        state: Union[Unset, str] = UNSET
        if not isinstance(self.state, Unset):
            state = self.state.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if billing_url is not UNSET:
            field_dict["billingUrl"] = billing_url
        if blocked_at is not UNSET:
            field_dict["blockedAt"] = blocked_at
        if grace_ends_at is not UNSET:
            field_dict["graceEndsAt"] = grace_ends_at
        if grace_started_at is not UNSET:
            field_dict["graceStartedAt"] = grace_started_at
        if state is not UNSET:
            field_dict["state"] = state

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        billing_url = d.pop("billingUrl", UNSET)

        def _parse_blocked_at(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        blocked_at = _parse_blocked_at(d.pop("blockedAt", UNSET))

        def _parse_grace_ends_at(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        grace_ends_at = _parse_grace_ends_at(d.pop("graceEndsAt", UNSET))

        def _parse_grace_started_at(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        grace_started_at = _parse_grace_started_at(d.pop("graceStartedAt", UNSET))

        _state = d.pop("state", UNSET)
        state: Union[Unset, GetPlanResponse200PaymentState]
        if isinstance(_state, Unset):
            state = UNSET
        else:
            state = GetPlanResponse200PaymentState(_state)

        get_plan_response_200_payment = cls(
            billing_url=billing_url,
            blocked_at=blocked_at,
            grace_ends_at=grace_ends_at,
            grace_started_at=grace_started_at,
            state=state,
        )

        get_plan_response_200_payment.additional_properties = d
        return get_plan_response_200_payment

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
