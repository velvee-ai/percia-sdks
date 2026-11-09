from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
    cast,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="AskSiteResponse200")


@_attrs_define
class AskSiteResponse200:
    """
    Attributes:
        answer (Union[Unset, str]):
        citations (Union[Unset, list[str]]):
    """

    answer: Union[Unset, str] = UNSET
    citations: Union[Unset, list[str]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        answer = self.answer

        citations: Union[Unset, list[str]] = UNSET
        if not isinstance(self.citations, Unset):
            citations = self.citations

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if answer is not UNSET:
            field_dict["answer"] = answer
        if citations is not UNSET:
            field_dict["citations"] = citations

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        answer = d.pop("answer", UNSET)

        citations = cast(list[str], d.pop("citations", UNSET))

        ask_site_response_200 = cls(
            answer=answer,
            citations=citations,
        )

        ask_site_response_200.additional_properties = d
        return ask_site_response_200

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
