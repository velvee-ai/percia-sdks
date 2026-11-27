from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
    cast,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.send_event_feedback_response_200_engine_type_0_state import (
    SendEventFeedbackResponse200EngineType0State,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="SendEventFeedbackResponse200EngineType0")


@_attrs_define
class SendEventFeedbackResponse200EngineType0:
    """
    Attributes:
        reason (Union[Unset, str]):
        state (Union[Unset, SendEventFeedbackResponse200EngineType0State]):
        words (Union[None, Unset, str]):
    """

    reason: Union[Unset, str] = UNSET
    state: Union[Unset, SendEventFeedbackResponse200EngineType0State] = UNSET
    words: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        reason = self.reason

        state: Union[Unset, str] = UNSET
        if not isinstance(self.state, Unset):
            state = self.state.value

        words: Union[None, Unset, str]
        if isinstance(self.words, Unset):
            words = UNSET
        else:
            words = self.words

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if reason is not UNSET:
            field_dict["reason"] = reason
        if state is not UNSET:
            field_dict["state"] = state
        if words is not UNSET:
            field_dict["words"] = words

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        reason = d.pop("reason", UNSET)

        _state = d.pop("state", UNSET)
        state: Union[Unset, SendEventFeedbackResponse200EngineType0State]
        if isinstance(_state, Unset):
            state = UNSET
        else:
            state = SendEventFeedbackResponse200EngineType0State(_state)

        def _parse_words(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        words = _parse_words(d.pop("words", UNSET))

        send_event_feedback_response_200_engine_type_0 = cls(
            reason=reason,
            state=state,
            words=words,
        )

        send_event_feedback_response_200_engine_type_0.additional_properties = d
        return send_event_feedback_response_200_engine_type_0

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
