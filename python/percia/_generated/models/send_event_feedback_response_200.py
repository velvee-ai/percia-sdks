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

from ..models.send_event_feedback_response_200_feedback import (
    SendEventFeedbackResponse200Feedback,
)
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.send_event_feedback_response_200_engine_type_0 import (
        SendEventFeedbackResponse200EngineType0,
    )
    from ..models.test_case_type_0 import TestCaseType0


T = TypeVar("T", bound="SendEventFeedbackResponse200")


@_attrs_define
class SendEventFeedbackResponse200:
    """
    Attributes:
        engine (Union['SendEventFeedbackResponse200EngineType0', None, Unset]):
        event_id (Union[Unset, str]):
        feedback (Union[Unset, SendEventFeedbackResponse200Feedback]):
        note (Union[None, Unset, str]):
        test_case (Union['TestCaseType0', None, Unset]):
    """

    engine: Union["SendEventFeedbackResponse200EngineType0", None, Unset] = UNSET
    event_id: Union[Unset, str] = UNSET
    feedback: Union[Unset, SendEventFeedbackResponse200Feedback] = UNSET
    note: Union[None, Unset, str] = UNSET
    test_case: Union["TestCaseType0", None, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.send_event_feedback_response_200_engine_type_0 import (
            SendEventFeedbackResponse200EngineType0,
        )
        from ..models.test_case_type_0 import TestCaseType0

        engine: Union[None, Unset, dict[str, Any]]
        if isinstance(self.engine, Unset):
            engine = UNSET
        elif isinstance(self.engine, SendEventFeedbackResponse200EngineType0):
            engine = self.engine.to_dict()
        else:
            engine = self.engine

        event_id = self.event_id

        feedback: Union[Unset, str] = UNSET
        if not isinstance(self.feedback, Unset):
            feedback = self.feedback.value

        note: Union[None, Unset, str]
        if isinstance(self.note, Unset):
            note = UNSET
        else:
            note = self.note

        test_case: Union[None, Unset, dict[str, Any]]
        if isinstance(self.test_case, Unset):
            test_case = UNSET
        elif isinstance(self.test_case, TestCaseType0):
            test_case = self.test_case.to_dict()
        else:
            test_case = self.test_case

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if engine is not UNSET:
            field_dict["engine"] = engine
        if event_id is not UNSET:
            field_dict["eventId"] = event_id
        if feedback is not UNSET:
            field_dict["feedback"] = feedback
        if note is not UNSET:
            field_dict["note"] = note
        if test_case is not UNSET:
            field_dict["testCase"] = test_case

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.send_event_feedback_response_200_engine_type_0 import (
            SendEventFeedbackResponse200EngineType0,
        )
        from ..models.test_case_type_0 import TestCaseType0

        d = dict(src_dict)

        def _parse_engine(
            data: object,
        ) -> Union["SendEventFeedbackResponse200EngineType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                engine_type_0 = SendEventFeedbackResponse200EngineType0.from_dict(data)

                return engine_type_0
            except:  # noqa: E722
                pass
            return cast(Union["SendEventFeedbackResponse200EngineType0", None, Unset], data)

        engine = _parse_engine(d.pop("engine", UNSET))

        event_id = d.pop("eventId", UNSET)

        _feedback = d.pop("feedback", UNSET)
        feedback: Union[Unset, SendEventFeedbackResponse200Feedback]
        if isinstance(_feedback, Unset):
            feedback = UNSET
        else:
            feedback = SendEventFeedbackResponse200Feedback(_feedback)

        def _parse_note(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        note = _parse_note(d.pop("note", UNSET))

        def _parse_test_case(data: object) -> Union["TestCaseType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_test_case_type_0 = TestCaseType0.from_dict(data)

                return componentsschemas_test_case_type_0
            except:  # noqa: E722
                pass
            return cast(Union["TestCaseType0", None, Unset], data)

        test_case = _parse_test_case(d.pop("testCase", UNSET))

        send_event_feedback_response_200 = cls(
            engine=engine,
            event_id=event_id,
            feedback=feedback,
            note=note,
            test_case=test_case,
        )

        send_event_feedback_response_200.additional_properties = d
        return send_event_feedback_response_200

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
