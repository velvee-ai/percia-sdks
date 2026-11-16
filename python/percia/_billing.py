"""Billing facts from ``GET /api/plan``, shaped like the ``billing`` block of MCP ``whoami``.

Every billing field is additive on the API: an older server omits some, so a missing field is ``None`` (booleans take the
safe value), never invented.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, List, Mapping, Optional, Tuple, Union


@dataclass(frozen=True)
class Billing:
    plan_label: Optional[str]  #: "Free" or "Pay as you go"
    free_minutes_remaining: Optional[int]  #: this month's free camera-minutes left (plus any unused card bonus)
    credit_minutes: Optional[int]  #: redeemed or granted minutes left (used before the free minutes)
    minutes_used_this_month: Optional[int]
    can_start_watches: (
        bool  #: False when billing or a failed payment blocks a new watch: check before ``watches.create``
    )
    how_charged: Optional[str]  #: one plain sentence
    next_step: Optional[str]  #: what to tell the person when watches cannot start or minutes are gone
    billing_url: Optional[str]
    payment_state: Optional[str]  #: "active", "grace" or "blocked"
    paid: bool  #: a card subscription is on file
    block_reason: Optional[str]  #: "needs_billing", "spend_cap" or None
    limits_note: Optional[str]
    bonus_available: bool  #: adding a card would still grant the one-time bonus
    bonus_minutes: Optional[int]
    has_card: bool
    free_minutes_resets_at: Optional[str]


def _int(v: Any) -> Optional[int]:
    return v if isinstance(v, int) and not isinstance(v, bool) else None


def _str(v: Any) -> Optional[str]:
    return v if isinstance(v, str) else None


def _one_of(v: Any, allowed: Tuple[str, ...]) -> Optional[str]:
    return v if isinstance(v, str) and v in allowed else None


def _as_dict(plan: Any) -> Mapping[str, Any]:
    if isinstance(plan, Mapping):
        return plan
    to_dict = getattr(plan, "to_dict", None)
    return to_dict() if callable(to_dict) else {}


def billing_of(plan: Union[Mapping[str, Any], Any]) -> Billing:
    """Read the billing facts out of a plan (the generated model or the JSON dict)."""
    p = _as_dict(plan)
    raw_payment = p.get("payment")
    payment: Mapping[str, Any] = raw_payment if isinstance(raw_payment, Mapping) else {}
    state = _one_of(payment.get("state"), ("active", "grace", "blocked"))
    reason = _one_of(p.get("blockReason"), ("needs_billing", "spend_cap"))
    return Billing(
        plan_label=_str(p.get("label")),
        free_minutes_remaining=_int(p.get("freeMinutesLeft")),
        credit_minutes=_int(p.get("creditMinutes")),
        minutes_used_this_month=_int(p.get("minutesUsedThisMonth")),
        can_start_watches=p.get("canStartWatches") is not False and state != "blocked",
        how_charged=_str(p.get("howCharged")),
        next_step=_str(p.get("nextStep")),
        billing_url=_str(p.get("billingUrl")) or _str(payment.get("billingUrl")),
        payment_state=state,
        paid=p.get("paid") is True,
        block_reason=reason,
        limits_note=_str(p.get("limitsNote")),
        bonus_available=p.get("bonusAvailable") is True,
        bonus_minutes=_int(p.get("bonusMinutes")),
        has_card=p.get("hasCard") is True or p.get("paid") is True,
        free_minutes_resets_at=_str(p.get("freeMinutesResetsAt")),
    )


def describe_billing(b: Billing) -> List[str]:
    """Plain lines for a person: plan, minutes, how charged, next step."""
    lines: List[str] = []
    if b.plan_label:
        lines.append(f"Plan:          {b.plan_label}{' (card on file)' if b.has_card else ''}")
    if b.free_minutes_remaining is not None:
        more = f" (more on {b.free_minutes_resets_at[:10]})" if b.free_minutes_resets_at else ""
        lines.append(f"Free minutes:  {b.free_minutes_remaining} left this month{more}")
    if b.credit_minutes is not None:
        lines.append(f"Credit:        {b.credit_minutes} minutes")
    if b.minutes_used_this_month is not None:
        lines.append(f"Used:          {b.minutes_used_this_month} minutes this month")
    if b.can_start_watches:
        lines.append("New watches:   can start")
    else:
        why = f" ({b.block_reason})" if b.block_reason else " (payment failed)" if b.payment_state == "blocked" else ""
        lines.append(f"New watches:   blocked{why}")
    if b.how_charged:
        lines.append(f"How charged:   {b.how_charged}")
    if b.bonus_available and b.bonus_minutes:
        lines.append(f"Card bonus:    {b.bonus_minutes} more free minutes once when you add a card")
    if b.next_step:
        lines.append(f"Next step:     {b.next_step}")
    if b.billing_url:
        lines.append(f"Billing:       {b.billing_url}")
    return lines
