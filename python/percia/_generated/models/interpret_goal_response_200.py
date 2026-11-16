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
    from ..models.interpret_goal_response_200_interpretation import (
        InterpretGoalResponse200Interpretation,
    )


T = TypeVar("T", bound="InterpretGoalResponse200")


@_attrs_define
class InterpretGoalResponse200:
    """
    Attributes:
        cached (Union[Unset, bool]):
        deferred (Union[Unset, bool]): Preview only, true when no model answered within the preview budget: the
            interpretation is the plain-words fallback, understand it on create instead.
        interpretation (Union[Unset, InterpretGoalResponse200Interpretation]):
    """

    cached: Union[Unset, bool] = UNSET
    deferred: Union[Unset, bool] = UNSET
    interpretation: Union[Unset, "InterpretGoalResponse200Interpretation"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        cached = self.cached

        deferred = self.deferred

        interpretation: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.interpretation, Unset):
            interpretation = self.interpretation.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if cached is not UNSET:
            field_dict["cached"] = cached
        if deferred is not UNSET:
            field_dict["deferred"] = deferred
        if interpretation is not UNSET:
            field_dict["interpretation"] = interpretation

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.interpret_goal_response_200_interpretation import (
            InterpretGoalResponse200Interpretation,
        )

        d = dict(src_dict)
        cached = d.pop("cached", UNSET)

        deferred = d.pop("deferred", UNSET)

        _interpretation = d.pop("interpretation", UNSET)
        interpretation: Union[Unset, InterpretGoalResponse200Interpretation]
        if isinstance(_interpretation, Unset):
            interpretation = UNSET
        else:
            interpretation = InterpretGoalResponse200Interpretation.from_dict(_interpretation)

        interpret_goal_response_200 = cls(
            cached=cached,
            deferred=deferred,
            interpretation=interpretation,
        )

        interpret_goal_response_200.additional_properties = d
        return interpret_goal_response_200

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
