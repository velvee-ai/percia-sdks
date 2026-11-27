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

T = TypeVar("T", bound="ListTestRunsResponse200TestsItemCaughtType0")


@_attrs_define
class ListTestRunsResponse200TestsItemCaughtType0:
    """
    Attributes:
        of (Union[None, Unset, int]):
        value (Union[Unset, int]):
    """

    of: Union[None, Unset, int] = UNSET
    value: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        of: Union[None, Unset, int]
        if isinstance(self.of, Unset):
            of = UNSET
        else:
            of = self.of

        value = self.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if of is not UNSET:
            field_dict["of"] = of
        if value is not UNSET:
            field_dict["value"] = value

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_of(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        of = _parse_of(d.pop("of", UNSET))

        value = d.pop("value", UNSET)

        list_test_runs_response_200_tests_item_caught_type_0 = cls(
            of=of,
            value=value,
        )

        list_test_runs_response_200_tests_item_caught_type_0.additional_properties = d
        return list_test_runs_response_200_tests_item_caught_type_0

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
