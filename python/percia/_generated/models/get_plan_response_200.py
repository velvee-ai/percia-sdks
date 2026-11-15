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

from ..models.get_plan_response_200_plan import GetPlanResponse200Plan
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.get_plan_response_200_counts import GetPlanResponse200Counts
    from ..models.get_plan_response_200_limits import GetPlanResponse200Limits
    from ..models.get_plan_response_200_month_to_date import (
        GetPlanResponse200MonthToDate,
    )
    from ..models.get_plan_response_200_payment import GetPlanResponse200Payment
    from ..models.get_plan_response_200_pricing import GetPlanResponse200Pricing


T = TypeVar("T", bound="GetPlanResponse200")


@_attrs_define
class GetPlanResponse200:
    """
    Attributes:
        billing_enforced (Union[Unset, bool]):
        cap_cents (Union[Unset, int]):
        counts (Union[Unset, GetPlanResponse200Counts]):
        credit_expires_at (Union[None, Unset, str]):
        credit_minutes (Union[Unset, int]): Redeemed or granted camera-minutes left (used first).
        enforced (Union[Unset, bool]):
        free_minutes (Union[Unset, int]):
        free_minutes_left (Union[Unset, int]):
        label (Union[Unset, str]): Shown name: Free or Pay as you go.
        limits (Union[Unset, GetPlanResponse200Limits]):
        month_to_date (Union[Unset, GetPlanResponse200MonthToDate]):
        payment (Union[Unset, GetPlanResponse200Payment]): Failed-payment state. state: active, grace (a payment failed;
            everything works until graceEndsAt) or blocked (writes answer 402 payment_required; update the payment method on
            the Billing page).
        plan (Union[Unset, GetPlanResponse200Plan]):
        pricing (Union[Unset, GetPlanResponse200Pricing]):
        selling (Union[Unset, bool]):
    """

    billing_enforced: Union[Unset, bool] = UNSET
    cap_cents: Union[Unset, int] = UNSET
    counts: Union[Unset, "GetPlanResponse200Counts"] = UNSET
    credit_expires_at: Union[None, Unset, str] = UNSET
    credit_minutes: Union[Unset, int] = UNSET
    enforced: Union[Unset, bool] = UNSET
    free_minutes: Union[Unset, int] = UNSET
    free_minutes_left: Union[Unset, int] = UNSET
    label: Union[Unset, str] = UNSET
    limits: Union[Unset, "GetPlanResponse200Limits"] = UNSET
    month_to_date: Union[Unset, "GetPlanResponse200MonthToDate"] = UNSET
    payment: Union[Unset, "GetPlanResponse200Payment"] = UNSET
    plan: Union[Unset, GetPlanResponse200Plan] = UNSET
    pricing: Union[Unset, "GetPlanResponse200Pricing"] = UNSET
    selling: Union[Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        billing_enforced = self.billing_enforced

        cap_cents = self.cap_cents

        counts: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.counts, Unset):
            counts = self.counts.to_dict()

        credit_expires_at: Union[None, Unset, str]
        if isinstance(self.credit_expires_at, Unset):
            credit_expires_at = UNSET
        else:
            credit_expires_at = self.credit_expires_at

        credit_minutes = self.credit_minutes

        enforced = self.enforced

        free_minutes = self.free_minutes

        free_minutes_left = self.free_minutes_left

        label = self.label

        limits: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.limits, Unset):
            limits = self.limits.to_dict()

        month_to_date: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.month_to_date, Unset):
            month_to_date = self.month_to_date.to_dict()

        payment: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.payment, Unset):
            payment = self.payment.to_dict()

        plan: Union[Unset, str] = UNSET
        if not isinstance(self.plan, Unset):
            plan = self.plan.value

        pricing: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.pricing, Unset):
            pricing = self.pricing.to_dict()

        selling = self.selling

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if billing_enforced is not UNSET:
            field_dict["billingEnforced"] = billing_enforced
        if cap_cents is not UNSET:
            field_dict["capCents"] = cap_cents
        if counts is not UNSET:
            field_dict["counts"] = counts
        if credit_expires_at is not UNSET:
            field_dict["creditExpiresAt"] = credit_expires_at
        if credit_minutes is not UNSET:
            field_dict["creditMinutes"] = credit_minutes
        if enforced is not UNSET:
            field_dict["enforced"] = enforced
        if free_minutes is not UNSET:
            field_dict["freeMinutes"] = free_minutes
        if free_minutes_left is not UNSET:
            field_dict["freeMinutesLeft"] = free_minutes_left
        if label is not UNSET:
            field_dict["label"] = label
        if limits is not UNSET:
            field_dict["limits"] = limits
        if month_to_date is not UNSET:
            field_dict["monthToDate"] = month_to_date
        if payment is not UNSET:
            field_dict["payment"] = payment
        if plan is not UNSET:
            field_dict["plan"] = plan
        if pricing is not UNSET:
            field_dict["pricing"] = pricing
        if selling is not UNSET:
            field_dict["selling"] = selling

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.get_plan_response_200_counts import GetPlanResponse200Counts
        from ..models.get_plan_response_200_limits import GetPlanResponse200Limits
        from ..models.get_plan_response_200_month_to_date import (
            GetPlanResponse200MonthToDate,
        )
        from ..models.get_plan_response_200_payment import GetPlanResponse200Payment
        from ..models.get_plan_response_200_pricing import GetPlanResponse200Pricing

        d = dict(src_dict)
        billing_enforced = d.pop("billingEnforced", UNSET)

        cap_cents = d.pop("capCents", UNSET)

        _counts = d.pop("counts", UNSET)
        counts: Union[Unset, GetPlanResponse200Counts]
        if isinstance(_counts, Unset):
            counts = UNSET
        else:
            counts = GetPlanResponse200Counts.from_dict(_counts)

        def _parse_credit_expires_at(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        credit_expires_at = _parse_credit_expires_at(d.pop("creditExpiresAt", UNSET))

        credit_minutes = d.pop("creditMinutes", UNSET)

        enforced = d.pop("enforced", UNSET)

        free_minutes = d.pop("freeMinutes", UNSET)

        free_minutes_left = d.pop("freeMinutesLeft", UNSET)

        label = d.pop("label", UNSET)

        _limits = d.pop("limits", UNSET)
        limits: Union[Unset, GetPlanResponse200Limits]
        if isinstance(_limits, Unset):
            limits = UNSET
        else:
            limits = GetPlanResponse200Limits.from_dict(_limits)

        _month_to_date = d.pop("monthToDate", UNSET)
        month_to_date: Union[Unset, GetPlanResponse200MonthToDate]
        if isinstance(_month_to_date, Unset):
            month_to_date = UNSET
        else:
            month_to_date = GetPlanResponse200MonthToDate.from_dict(_month_to_date)

        _payment = d.pop("payment", UNSET)
        payment: Union[Unset, GetPlanResponse200Payment]
        if isinstance(_payment, Unset):
            payment = UNSET
        else:
            payment = GetPlanResponse200Payment.from_dict(_payment)

        _plan = d.pop("plan", UNSET)
        plan: Union[Unset, GetPlanResponse200Plan]
        if isinstance(_plan, Unset):
            plan = UNSET
        else:
            plan = GetPlanResponse200Plan(_plan)

        _pricing = d.pop("pricing", UNSET)
        pricing: Union[Unset, GetPlanResponse200Pricing]
        if isinstance(_pricing, Unset):
            pricing = UNSET
        else:
            pricing = GetPlanResponse200Pricing.from_dict(_pricing)

        selling = d.pop("selling", UNSET)

        get_plan_response_200 = cls(
            billing_enforced=billing_enforced,
            cap_cents=cap_cents,
            counts=counts,
            credit_expires_at=credit_expires_at,
            credit_minutes=credit_minutes,
            enforced=enforced,
            free_minutes=free_minutes,
            free_minutes_left=free_minutes_left,
            label=label,
            limits=limits,
            month_to_date=month_to_date,
            payment=payment,
            plan=plan,
            pricing=pricing,
            selling=selling,
        )

        get_plan_response_200.additional_properties = d
        return get_plan_response_200

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
