from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.send_event_feedback_body_verdict import SendEventFeedbackBodyVerdict
from ..types import UNSET, Unset

T = TypeVar("T", bound="SendEventFeedbackBody")


@_attrs_define
class SendEventFeedbackBody:
    """
    Attributes:
        verdict (SendEventFeedbackBodyVerdict):
        note (Union[Unset, str]):
    """

    verdict: SendEventFeedbackBodyVerdict
    note: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        verdict = self.verdict.value

        note = self.note

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "verdict": verdict,
            }
        )
        if note is not UNSET:
            field_dict["note"] = note

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        verdict = SendEventFeedbackBodyVerdict(d.pop("verdict"))

        note = d.pop("note", UNSET)

        send_event_feedback_body = cls(
            verdict=verdict,
            note=note,
        )

        send_event_feedback_body.additional_properties = d
        return send_event_feedback_body

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
