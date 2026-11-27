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

from ..models.list_near_misses_response_200_suggestions_item_why import (
    ListNearMissesResponse200SuggestionsItemWhy,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="ListNearMissesResponse200SuggestionsItem")


@_attrs_define
class ListNearMissesResponse200SuggestionsItem:
    """
    Attributes:
        at (Union[Unset, datetime.datetime]):
        confidence (Union[None, Unset, float]):
        event_id (Union[None, Unset, str]): Set for a close call or false alarm.
        miss_id (Union[None, Unset, str]): Set for a reported miss.
        text (Union[Unset, str]):
        why (Union[Unset, ListNearMissesResponse200SuggestionsItemWhy]):
    """

    at: Union[Unset, datetime.datetime] = UNSET
    confidence: Union[None, Unset, float] = UNSET
    event_id: Union[None, Unset, str] = UNSET
    miss_id: Union[None, Unset, str] = UNSET
    text: Union[Unset, str] = UNSET
    why: Union[Unset, ListNearMissesResponse200SuggestionsItemWhy] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        at: Union[Unset, str] = UNSET
        if not isinstance(self.at, Unset):
            at = self.at.isoformat()

        confidence: Union[None, Unset, float]
        if isinstance(self.confidence, Unset):
            confidence = UNSET
        else:
            confidence = self.confidence

        event_id: Union[None, Unset, str]
        if isinstance(self.event_id, Unset):
            event_id = UNSET
        else:
            event_id = self.event_id

        miss_id: Union[None, Unset, str]
        if isinstance(self.miss_id, Unset):
            miss_id = UNSET
        else:
            miss_id = self.miss_id

        text = self.text

        why: Union[Unset, str] = UNSET
        if not isinstance(self.why, Unset):
            why = self.why.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if at is not UNSET:
            field_dict["at"] = at
        if confidence is not UNSET:
            field_dict["confidence"] = confidence
        if event_id is not UNSET:
            field_dict["eventId"] = event_id
        if miss_id is not UNSET:
            field_dict["missId"] = miss_id
        if text is not UNSET:
            field_dict["text"] = text
        if why is not UNSET:
            field_dict["why"] = why

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _at = d.pop("at", UNSET)
        at: Union[Unset, datetime.datetime]
        if isinstance(_at, Unset):
            at = UNSET
        else:
            at = isoparse(_at)

        def _parse_confidence(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        confidence = _parse_confidence(d.pop("confidence", UNSET))

        def _parse_event_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        event_id = _parse_event_id(d.pop("eventId", UNSET))

        def _parse_miss_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        miss_id = _parse_miss_id(d.pop("missId", UNSET))

        text = d.pop("text", UNSET)

        _why = d.pop("why", UNSET)
        why: Union[Unset, ListNearMissesResponse200SuggestionsItemWhy]
        if isinstance(_why, Unset):
            why = UNSET
        else:
            why = ListNearMissesResponse200SuggestionsItemWhy(_why)

        list_near_misses_response_200_suggestions_item = cls(
            at=at,
            confidence=confidence,
            event_id=event_id,
            miss_id=miss_id,
            text=text,
            why=why,
        )

        list_near_misses_response_200_suggestions_item.additional_properties = d
        return list_near_misses_response_200_suggestions_item

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
