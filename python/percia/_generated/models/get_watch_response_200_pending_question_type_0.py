import datetime
from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
    cast,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="GetWatchResponse200PendingQuestionType0")


@_attrs_define
class GetWatchResponse200PendingQuestionType0:
    """Detail only. A converted watch that waits for an answer: the question, its options (may be empty), when it was asked
    and the draft to answer through POST /watches/draft/{draftId}/answer. Null otherwise.

        Attributes:
            asked_at (Union[Unset, datetime.datetime]):
            draft_id (Union[Unset, str]):
            options (Union[Unset, list[str]]):
            question (Union[Unset, str]):
    """

    asked_at: Union[Unset, datetime.datetime] = UNSET
    draft_id: Union[Unset, str] = UNSET
    options: Union[Unset, list[str]] = UNSET
    question: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        asked_at: Union[Unset, str] = UNSET
        if not isinstance(self.asked_at, Unset):
            asked_at = self.asked_at.isoformat()

        draft_id = self.draft_id

        options: Union[Unset, list[str]] = UNSET
        if not isinstance(self.options, Unset):
            options = self.options

        question = self.question

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if asked_at is not UNSET:
            field_dict["askedAt"] = asked_at
        if draft_id is not UNSET:
            field_dict["draftId"] = draft_id
        if options is not UNSET:
            field_dict["options"] = options
        if question is not UNSET:
            field_dict["question"] = question

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _asked_at = d.pop("askedAt", UNSET)
        asked_at: Union[Unset, datetime.datetime]
        if isinstance(_asked_at, Unset):
            asked_at = UNSET
        else:
            asked_at = isoparse(_asked_at)

        draft_id = d.pop("draftId", UNSET)

        options = cast(list[str], d.pop("options", UNSET))

        question = d.pop("question", UNSET)

        get_watch_response_200_pending_question_type_0 = cls(
            asked_at=asked_at,
            draft_id=draft_id,
            options=options,
            question=question,
        )

        get_watch_response_200_pending_question_type_0.additional_properties = d
        return get_watch_response_200_pending_question_type_0

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
