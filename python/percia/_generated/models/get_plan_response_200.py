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

from ..models.get_plan_response_200_block_reason_type_1 import (
    GetPlanResponse200BlockReasonType1,
)
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
        block_reason (Union[GetPlanResponse200BlockReasonType1, None, Unset]): Why a new watch is refused for billing
            right now; null when none (always null while billing is not enforced).
        bonus_available (Union[Unset, bool]): True while adding a card would still grant the one-time bonus.
        bonus_minutes (Union[Unset, int]):
        bonus_minutes_left (Union[Unset, int]):
        can_start_watches (Union[Unset, bool]): False when billing or a failed payment blocks a new watch now.
        cap_cents (Union[Unset, int]):
        counts (Union[Unset, GetPlanResponse200Counts]):
        credit_expires_at (Union[None, Unset, str]):
        credit_minutes (Union[Unset, int]): Redeemed or granted camera-minutes left (used first).
        enforced (Union[Unset, bool]):
        free_minutes (Union[Unset, int]):
        free_minutes_left (Union[Unset, int]): Free minutes left: this month's 10 plus any one-time card bonus not yet
            used.
        free_minutes_resets_at (Union[Unset, str]): When the monthly free minutes come back (the 1st of the next UTC
            month).
        has_card (Union[Unset, bool]):
        how_charged (Union[Unset, str]): One plain sentence on how this account is charged.
        label (Union[Unset, str]): Shown name: Free or Pay as you go.
        limits (Union[Unset, GetPlanResponse200Limits]):
        limits_note (Union[Unset, str]): What the plan-count limits mean now: minutes are the real limit; counts are
            informational unless enforced is true.
        minutes_used_this_month (Union[Unset, int]):
        month_to_date (Union[Unset, GetPlanResponse200MonthToDate]):
        next_step (Union[None, Unset, str]): What to tell the person when canStartWatches is false or minutes are gone.
        paid (Union[Unset, bool]): A card subscription is on file.
        payment (Union[Unset, GetPlanResponse200Payment]): Failed-payment state. state: active, grace (a payment failed;
            everything works until graceEndsAt) or blocked (writes answer 402 payment_required; update the payment method on
            the Billing page).
        plan (Union[Unset, GetPlanResponse200Plan]):
        pricing (Union[Unset, GetPlanResponse200Pricing]):
        selling (Union[Unset, bool]):
    """

    billing_enforced: Union[Unset, bool] = UNSET
    block_reason: Union[GetPlanResponse200BlockReasonType1, None, Unset] = UNSET
    bonus_available: Union[Unset, bool] = UNSET
    bonus_minutes: Union[Unset, int] = UNSET
    bonus_minutes_left: Union[Unset, int] = UNSET
    can_start_watches: Union[Unset, bool] = UNSET
    cap_cents: Union[Unset, int] = UNSET
    counts: Union[Unset, "GetPlanResponse200Counts"] = UNSET
    credit_expires_at: Union[None, Unset, str] = UNSET
    credit_minutes: Union[Unset, int] = UNSET
    enforced: Union[Unset, bool] = UNSET
    free_minutes: Union[Unset, int] = UNSET
    free_minutes_left: Union[Unset, int] = UNSET
    free_minutes_resets_at: Union[Unset, str] = UNSET
    has_card: Union[Unset, bool] = UNSET
    how_charged: Union[Unset, str] = UNSET
    label: Union[Unset, str] = UNSET
    limits: Union[Unset, "GetPlanResponse200Limits"] = UNSET
    limits_note: Union[Unset, str] = UNSET
    minutes_used_this_month: Union[Unset, int] = UNSET
    month_to_date: Union[Unset, "GetPlanResponse200MonthToDate"] = UNSET
    next_step: Union[None, Unset, str] = UNSET
    paid: Union[Unset, bool] = UNSET
    payment: Union[Unset, "GetPlanResponse200Payment"] = UNSET
    plan: Union[Unset, GetPlanResponse200Plan] = UNSET
    pricing: Union[Unset, "GetPlanResponse200Pricing"] = UNSET
    selling: Union[Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        billing_enforced = self.billing_enforced

        block_reason: Union[None, Unset, str]
        if isinstance(self.block_reason, Unset):
            block_reason = UNSET
        elif isinstance(self.block_reason, GetPlanResponse200BlockReasonType1):
            block_reason = self.block_reason.value
        else:
            block_reason = self.block_reason

        bonus_available = self.bonus_available

        bonus_minutes = self.bonus_minutes

        bonus_minutes_left = self.bonus_minutes_left

        can_start_watches = self.can_start_watches

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

        free_minutes_resets_at = self.free_minutes_resets_at

        has_card = self.has_card

        how_charged = self.how_charged

        label = self.label

        limits: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.limits, Unset):
            limits = self.limits.to_dict()

        limits_note = self.limits_note

        minutes_used_this_month = self.minutes_used_this_month

        month_to_date: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.month_to_date, Unset):
            month_to_date = self.month_to_date.to_dict()

        next_step: Union[None, Unset, str]
        if isinstance(self.next_step, Unset):
            next_step = UNSET
        else:
            next_step = self.next_step

        paid = self.paid

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
        if block_reason is not UNSET:
            field_dict["blockReason"] = block_reason
        if bonus_available is not UNSET:
            field_dict["bonusAvailable"] = bonus_available
        if bonus_minutes is not UNSET:
            field_dict["bonusMinutes"] = bonus_minutes
        if bonus_minutes_left is not UNSET:
            field_dict["bonusMinutesLeft"] = bonus_minutes_left
        if can_start_watches is not UNSET:
            field_dict["canStartWatches"] = can_start_watches
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
        if free_minutes_resets_at is not UNSET:
            field_dict["freeMinutesResetsAt"] = free_minutes_resets_at
        if has_card is not UNSET:
            field_dict["hasCard"] = has_card
        if how_charged is not UNSET:
            field_dict["howCharged"] = how_charged
        if label is not UNSET:
            field_dict["label"] = label
        if limits is not UNSET:
            field_dict["limits"] = limits
        if limits_note is not UNSET:
            field_dict["limitsNote"] = limits_note
        if minutes_used_this_month is not UNSET:
            field_dict["minutesUsedThisMonth"] = minutes_used_this_month
        if month_to_date is not UNSET:
            field_dict["monthToDate"] = month_to_date
        if next_step is not UNSET:
            field_dict["nextStep"] = next_step
        if paid is not UNSET:
            field_dict["paid"] = paid
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

        def _parse_block_reason(
            data: object,
        ) -> Union[GetPlanResponse200BlockReasonType1, None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                block_reason_type_1 = GetPlanResponse200BlockReasonType1(data)

                return block_reason_type_1
            except:  # noqa: E722
                pass
            return cast(Union[GetPlanResponse200BlockReasonType1, None, Unset], data)

        block_reason = _parse_block_reason(d.pop("blockReason", UNSET))

        bonus_available = d.pop("bonusAvailable", UNSET)

        bonus_minutes = d.pop("bonusMinutes", UNSET)

        bonus_minutes_left = d.pop("bonusMinutesLeft", UNSET)

        can_start_watches = d.pop("canStartWatches", UNSET)

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

        free_minutes_resets_at = d.pop("freeMinutesResetsAt", UNSET)

        has_card = d.pop("hasCard", UNSET)

        how_charged = d.pop("howCharged", UNSET)

        label = d.pop("label", UNSET)

        _limits = d.pop("limits", UNSET)
        limits: Union[Unset, GetPlanResponse200Limits]
        if isinstance(_limits, Unset):
            limits = UNSET
        else:
            limits = GetPlanResponse200Limits.from_dict(_limits)

        limits_note = d.pop("limitsNote", UNSET)

        minutes_used_this_month = d.pop("minutesUsedThisMonth", UNSET)

        _month_to_date = d.pop("monthToDate", UNSET)
        month_to_date: Union[Unset, GetPlanResponse200MonthToDate]
        if isinstance(_month_to_date, Unset):
            month_to_date = UNSET
        else:
            month_to_date = GetPlanResponse200MonthToDate.from_dict(_month_to_date)

        def _parse_next_step(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        next_step = _parse_next_step(d.pop("nextStep", UNSET))

        paid = d.pop("paid", UNSET)

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
            block_reason=block_reason,
            bonus_available=bonus_available,
            bonus_minutes=bonus_minutes,
            bonus_minutes_left=bonus_minutes_left,
            can_start_watches=can_start_watches,
            cap_cents=cap_cents,
            counts=counts,
            credit_expires_at=credit_expires_at,
            credit_minutes=credit_minutes,
            enforced=enforced,
            free_minutes=free_minutes,
            free_minutes_left=free_minutes_left,
            free_minutes_resets_at=free_minutes_resets_at,
            has_card=has_card,
            how_charged=how_charged,
            label=label,
            limits=limits,
            limits_note=limits_note,
            minutes_used_this_month=minutes_used_this_month,
            month_to_date=month_to_date,
            next_step=next_step,
            paid=paid,
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
