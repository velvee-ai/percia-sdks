from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ListDatasetClipsResponse200Counts")


@_attrs_define
class ListDatasetClipsResponse200Counts:
    """
    Attributes:
        counterfactual (Union[Unset, int]):
        should_match (Union[Unset, int]):
        should_not (Union[Unset, int]):
    """

    counterfactual: Union[Unset, int] = UNSET
    should_match: Union[Unset, int] = UNSET
    should_not: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        counterfactual = self.counterfactual

        should_match = self.should_match

        should_not = self.should_not

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if counterfactual is not UNSET:
            field_dict["counterfactual"] = counterfactual
        if should_match is not UNSET:
            field_dict["should_match"] = should_match
        if should_not is not UNSET:
            field_dict["should_not"] = should_not

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        counterfactual = d.pop("counterfactual", UNSET)

        should_match = d.pop("should_match", UNSET)

        should_not = d.pop("should_not", UNSET)

        list_dataset_clips_response_200_counts = cls(
            counterfactual=counterfactual,
            should_match=should_match,
            should_not=should_not,
        )

        list_dataset_clips_response_200_counts.additional_properties = d
        return list_dataset_clips_response_200_counts

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
