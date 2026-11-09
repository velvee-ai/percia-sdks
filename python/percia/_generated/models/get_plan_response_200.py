from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.get_plan_response_200_plan import GetPlanResponse200Plan
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.get_plan_response_200_counts import GetPlanResponse200Counts
    from ..models.get_plan_response_200_limits import GetPlanResponse200Limits


T = TypeVar("T", bound="GetPlanResponse200")


@_attrs_define
class GetPlanResponse200:
    """
    Attributes:
        counts (Union[Unset, GetPlanResponse200Counts]):
        enforced (Union[Unset, bool]):
        limits (Union[Unset, GetPlanResponse200Limits]):
        plan (Union[Unset, GetPlanResponse200Plan]):
        selling (Union[Unset, bool]):
    """

    counts: Union[Unset, "GetPlanResponse200Counts"] = UNSET
    enforced: Union[Unset, bool] = UNSET
    limits: Union[Unset, "GetPlanResponse200Limits"] = UNSET
    plan: Union[Unset, GetPlanResponse200Plan] = UNSET
    selling: Union[Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        counts: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.counts, Unset):
            counts = self.counts.to_dict()

        enforced = self.enforced

        limits: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.limits, Unset):
            limits = self.limits.to_dict()

        plan: Union[Unset, str] = UNSET
        if not isinstance(self.plan, Unset):
            plan = self.plan.value

        selling = self.selling

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if counts is not UNSET:
            field_dict["counts"] = counts
        if enforced is not UNSET:
            field_dict["enforced"] = enforced
        if limits is not UNSET:
            field_dict["limits"] = limits
        if plan is not UNSET:
            field_dict["plan"] = plan
        if selling is not UNSET:
            field_dict["selling"] = selling

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.get_plan_response_200_counts import GetPlanResponse200Counts
        from ..models.get_plan_response_200_limits import GetPlanResponse200Limits

        d = dict(src_dict)
        _counts = d.pop("counts", UNSET)
        counts: Union[Unset, GetPlanResponse200Counts]
        if isinstance(_counts, Unset):
            counts = UNSET
        else:
            counts = GetPlanResponse200Counts.from_dict(_counts)

        enforced = d.pop("enforced", UNSET)

        _limits = d.pop("limits", UNSET)
        limits: Union[Unset, GetPlanResponse200Limits]
        if isinstance(_limits, Unset):
            limits = UNSET
        else:
            limits = GetPlanResponse200Limits.from_dict(_limits)

        _plan = d.pop("plan", UNSET)
        plan: Union[Unset, GetPlanResponse200Plan]
        if isinstance(_plan, Unset):
            plan = UNSET
        else:
            plan = GetPlanResponse200Plan(_plan)

        selling = d.pop("selling", UNSET)

        get_plan_response_200 = cls(
            counts=counts,
            enforced=enforced,
            limits=limits,
            plan=plan,
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
