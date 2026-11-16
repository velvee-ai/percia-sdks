from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="TestRunInterpretationType0")


@_attrs_define
class TestRunInterpretationType0:
    """What Percia understands of the goal (additive; null on a watch created before goal understanding, with an agent, on
    Percia core, or with interpret false and no kind). version, shape (narrow, compound, open_ended), summary, kind
    (state = something stays true, event = something happens, mixed), concerns [{id, text, kind, evidence, ignore}] (the
    conditions the watch runs), assumptions, gaps [{description, reason, question}] (what a camera cannot see or the
    goal leaves open: ask the person the questions), untestable (words a camera cannot judge), confidence, clarity
    (0..1), cadence (a suggestion, not applied), source (model, rules, user, agent), degraded (null, or why Percia used
    the words as written: unavailable, invalid, quota, killed, review_skipped), needsLook, applied, createdAt,
    reviewedAt. Event kind is the one that fires on arrivals; kind is an intent hint the engine may override.

    """

    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        test_run_interpretation_type_0 = cls()

        test_run_interpretation_type_0.additional_properties = d
        return test_run_interpretation_type_0

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
