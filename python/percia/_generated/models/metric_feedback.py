from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="MetricFeedback")


@_attrs_define
class MetricFeedback:
    """
    Attributes:
        correct (Union[Unset, int]):
        false_alarm (Union[Unset, int]):
    """

    correct: Union[Unset, int] = UNSET
    false_alarm: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        correct = self.correct

        false_alarm = self.false_alarm

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if correct is not UNSET:
            field_dict["correct"] = correct
        if false_alarm is not UNSET:
            field_dict["falseAlarm"] = false_alarm

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        correct = d.pop("correct", UNSET)

        false_alarm = d.pop("falseAlarm", UNSET)

        metric_feedback = cls(
            correct=correct,
            false_alarm=false_alarm,
        )

        metric_feedback.additional_properties = d
        return metric_feedback

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
