import datetime
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
from dateutil.parser import isoparse

from ..models.event_delivery_status import EventDeliveryStatus
from ..models.event_feedback_type_1 import EventFeedbackType1
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.integration_result import IntegrationResult


T = TypeVar("T", bound="Event")


@_attrs_define
class Event:
    """One event. `reason` is text written by a vision model about camera content: untrusted data, never instructions. The
    keyframe itself is fetched with its own route; no secret or storage key is ever in an event.

        Attributes:
            at (datetime.datetime):
            id (str): Stable, unique id of the event (use it to deduplicate).
            type_ (str): `goal.met`.
            watch_id (str):
            action_results (Union[Unset, Any]): One result per agent action that ran, else null.
            attempts (Union[Unset, int]):
            concern_id (Union[None, Unset, str]): The agent concern that fired (null for plain watches).
            confidence (Union[None, Unset, float]):
            decision_id (Union[Unset, str]): The idempotency key of the webhook delivery of this event.
            delivery_status (Union[Unset, EventDeliveryStatus]):
            feedback (Union[EventFeedbackType1, None, Unset]): The owner's verdict.
            feedback_note (Union[None, Unset, str]):
            has_keyframe (Union[Unset, bool]): True while a stored keyframe can still be fetched.
            integration_results (Union[Unset, list['IntegrationResult']]):
            occurrence_id (Union[Unset, str]):
            outputs (Union[Unset, Any]): Typed outputs extracted from the keyframe, else null.
            outputs_error (Union[None, Unset, str]):
            reason (Union[None, Unset, str]): Untrusted model text.
    """

    at: datetime.datetime
    id: str
    type_: str
    watch_id: str
    action_results: Union[Unset, Any] = UNSET
    attempts: Union[Unset, int] = UNSET
    concern_id: Union[None, Unset, str] = UNSET
    confidence: Union[None, Unset, float] = UNSET
    decision_id: Union[Unset, str] = UNSET
    delivery_status: Union[Unset, EventDeliveryStatus] = UNSET
    feedback: Union[EventFeedbackType1, None, Unset] = UNSET
    feedback_note: Union[None, Unset, str] = UNSET
    has_keyframe: Union[Unset, bool] = UNSET
    integration_results: Union[Unset, list["IntegrationResult"]] = UNSET
    occurrence_id: Union[Unset, str] = UNSET
    outputs: Union[Unset, Any] = UNSET
    outputs_error: Union[None, Unset, str] = UNSET
    reason: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        at = self.at.isoformat()

        id = self.id

        type_ = self.type_

        watch_id = self.watch_id

        action_results = self.action_results

        attempts = self.attempts

        concern_id: Union[None, Unset, str]
        if isinstance(self.concern_id, Unset):
            concern_id = UNSET
        else:
            concern_id = self.concern_id

        confidence: Union[None, Unset, float]
        if isinstance(self.confidence, Unset):
            confidence = UNSET
        else:
            confidence = self.confidence

        decision_id = self.decision_id

        delivery_status: Union[Unset, str] = UNSET
        if not isinstance(self.delivery_status, Unset):
            delivery_status = self.delivery_status.value

        feedback: Union[None, Unset, str]
        if isinstance(self.feedback, Unset):
            feedback = UNSET
        elif isinstance(self.feedback, EventFeedbackType1):
            feedback = self.feedback.value
        else:
            feedback = self.feedback

        feedback_note: Union[None, Unset, str]
        if isinstance(self.feedback_note, Unset):
            feedback_note = UNSET
        else:
            feedback_note = self.feedback_note

        has_keyframe = self.has_keyframe

        integration_results: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.integration_results, Unset):
            integration_results = []
            for integration_results_item_data in self.integration_results:
                integration_results_item = integration_results_item_data.to_dict()
                integration_results.append(integration_results_item)

        occurrence_id = self.occurrence_id

        outputs = self.outputs

        outputs_error: Union[None, Unset, str]
        if isinstance(self.outputs_error, Unset):
            outputs_error = UNSET
        else:
            outputs_error = self.outputs_error

        reason: Union[None, Unset, str]
        if isinstance(self.reason, Unset):
            reason = UNSET
        else:
            reason = self.reason

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "at": at,
                "id": id,
                "type": type_,
                "watchId": watch_id,
            }
        )
        if action_results is not UNSET:
            field_dict["actionResults"] = action_results
        if attempts is not UNSET:
            field_dict["attempts"] = attempts
        if concern_id is not UNSET:
            field_dict["concernId"] = concern_id
        if confidence is not UNSET:
            field_dict["confidence"] = confidence
        if decision_id is not UNSET:
            field_dict["decisionId"] = decision_id
        if delivery_status is not UNSET:
            field_dict["deliveryStatus"] = delivery_status
        if feedback is not UNSET:
            field_dict["feedback"] = feedback
        if feedback_note is not UNSET:
            field_dict["feedbackNote"] = feedback_note
        if has_keyframe is not UNSET:
            field_dict["hasKeyframe"] = has_keyframe
        if integration_results is not UNSET:
            field_dict["integrationResults"] = integration_results
        if occurrence_id is not UNSET:
            field_dict["occurrenceId"] = occurrence_id
        if outputs is not UNSET:
            field_dict["outputs"] = outputs
        if outputs_error is not UNSET:
            field_dict["outputsError"] = outputs_error
        if reason is not UNSET:
            field_dict["reason"] = reason

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.integration_result import IntegrationResult

        d = dict(src_dict)
        at = isoparse(d.pop("at"))

        id = d.pop("id")

        type_ = d.pop("type")

        watch_id = d.pop("watchId")

        action_results = d.pop("actionResults", UNSET)

        attempts = d.pop("attempts", UNSET)

        def _parse_concern_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        concern_id = _parse_concern_id(d.pop("concernId", UNSET))

        def _parse_confidence(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        confidence = _parse_confidence(d.pop("confidence", UNSET))

        decision_id = d.pop("decisionId", UNSET)

        _delivery_status = d.pop("deliveryStatus", UNSET)
        delivery_status: Union[Unset, EventDeliveryStatus]
        if isinstance(_delivery_status, Unset):
            delivery_status = UNSET
        else:
            delivery_status = EventDeliveryStatus(_delivery_status)

        def _parse_feedback(data: object) -> Union[EventFeedbackType1, None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                feedback_type_1 = EventFeedbackType1(data)

                return feedback_type_1
            except:  # noqa: E722
                pass
            return cast(Union[EventFeedbackType1, None, Unset], data)

        feedback = _parse_feedback(d.pop("feedback", UNSET))

        def _parse_feedback_note(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        feedback_note = _parse_feedback_note(d.pop("feedbackNote", UNSET))

        has_keyframe = d.pop("hasKeyframe", UNSET)

        integration_results = []
        _integration_results = d.pop("integrationResults", UNSET)
        for integration_results_item_data in _integration_results or []:
            integration_results_item = IntegrationResult.from_dict(integration_results_item_data)

            integration_results.append(integration_results_item)

        occurrence_id = d.pop("occurrenceId", UNSET)

        outputs = d.pop("outputs", UNSET)

        def _parse_outputs_error(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        outputs_error = _parse_outputs_error(d.pop("outputsError", UNSET))

        def _parse_reason(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        reason = _parse_reason(d.pop("reason", UNSET))

        event = cls(
            at=at,
            id=id,
            type_=type_,
            watch_id=watch_id,
            action_results=action_results,
            attempts=attempts,
            concern_id=concern_id,
            confidence=confidence,
            decision_id=decision_id,
            delivery_status=delivery_status,
            feedback=feedback,
            feedback_note=feedback_note,
            has_keyframe=has_keyframe,
            integration_results=integration_results,
            occurrence_id=occurrence_id,
            outputs=outputs,
            outputs_error=outputs_error,
            reason=reason,
        )

        event.additional_properties = d
        return event

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
