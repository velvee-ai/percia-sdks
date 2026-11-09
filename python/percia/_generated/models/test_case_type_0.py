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

from ..models.test_case_type_0_expected import TestCaseType0Expected
from ..types import UNSET, Unset

T = TypeVar("T", bound="TestCaseType0")


@_attrs_define
class TestCaseType0:
    """
    Attributes:
        agent_id (Union[None, Unset, str]):
        concern_id (Union[None, Unset, str]):
        concern_text (Union[Unset, str]):
        created_at (Union[Unset, datetime.datetime]):
        event_id (Union[Unset, str]):
        expected (Union[Unset, TestCaseType0Expected]):
        id (Union[Unset, str]):
        note (Union[Unset, str]):
        watch_id (Union[Unset, str]):
    """

    agent_id: Union[None, Unset, str] = UNSET
    concern_id: Union[None, Unset, str] = UNSET
    concern_text: Union[Unset, str] = UNSET
    created_at: Union[Unset, datetime.datetime] = UNSET
    event_id: Union[Unset, str] = UNSET
    expected: Union[Unset, TestCaseType0Expected] = UNSET
    id: Union[Unset, str] = UNSET
    note: Union[Unset, str] = UNSET
    watch_id: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        agent_id: Union[None, Unset, str]
        if isinstance(self.agent_id, Unset):
            agent_id = UNSET
        else:
            agent_id = self.agent_id

        concern_id: Union[None, Unset, str]
        if isinstance(self.concern_id, Unset):
            concern_id = UNSET
        else:
            concern_id = self.concern_id

        concern_text = self.concern_text

        created_at: Union[Unset, str] = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()

        event_id = self.event_id

        expected: Union[Unset, str] = UNSET
        if not isinstance(self.expected, Unset):
            expected = self.expected.value

        id = self.id

        note = self.note

        watch_id = self.watch_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if agent_id is not UNSET:
            field_dict["agentId"] = agent_id
        if concern_id is not UNSET:
            field_dict["concernId"] = concern_id
        if concern_text is not UNSET:
            field_dict["concernText"] = concern_text
        if created_at is not UNSET:
            field_dict["createdAt"] = created_at
        if event_id is not UNSET:
            field_dict["eventId"] = event_id
        if expected is not UNSET:
            field_dict["expected"] = expected
        if id is not UNSET:
            field_dict["id"] = id
        if note is not UNSET:
            field_dict["note"] = note
        if watch_id is not UNSET:
            field_dict["watchId"] = watch_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_agent_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        agent_id = _parse_agent_id(d.pop("agentId", UNSET))

        def _parse_concern_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        concern_id = _parse_concern_id(d.pop("concernId", UNSET))

        concern_text = d.pop("concernText", UNSET)

        _created_at = d.pop("createdAt", UNSET)
        created_at: Union[Unset, datetime.datetime]
        if isinstance(_created_at, Unset):
            created_at = UNSET
        else:
            created_at = isoparse(_created_at)

        event_id = d.pop("eventId", UNSET)

        _expected = d.pop("expected", UNSET)
        expected: Union[Unset, TestCaseType0Expected]
        if isinstance(_expected, Unset):
            expected = UNSET
        else:
            expected = TestCaseType0Expected(_expected)

        id = d.pop("id", UNSET)

        note = d.pop("note", UNSET)

        watch_id = d.pop("watchId", UNSET)

        test_case_type_0 = cls(
            agent_id=agent_id,
            concern_id=concern_id,
            concern_text=concern_text,
            created_at=created_at,
            event_id=event_id,
            expected=expected,
            id=id,
            note=note,
            watch_id=watch_id,
        )

        test_case_type_0.additional_properties = d
        return test_case_type_0

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
