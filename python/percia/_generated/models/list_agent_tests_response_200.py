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

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.test_case_type_0 import TestCaseType0


T = TypeVar("T", bound="ListAgentTestsResponse200")


@_attrs_define
class ListAgentTestsResponse200:
    """
    Attributes:
        cases (Union[Unset, list[Union['TestCaseType0', None]]]):
    """

    cases: Union[Unset, list[Union["TestCaseType0", None]]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.test_case_type_0 import TestCaseType0

        cases: Union[Unset, list[Union[None, dict[str, Any]]]] = UNSET
        if not isinstance(self.cases, Unset):
            cases = []
            for cases_item_data in self.cases:
                cases_item: Union[None, dict[str, Any]]
                if isinstance(cases_item_data, TestCaseType0):
                    cases_item = cases_item_data.to_dict()
                else:
                    cases_item = cases_item_data
                cases.append(cases_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if cases is not UNSET:
            field_dict["cases"] = cases

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.test_case_type_0 import TestCaseType0

        d = dict(src_dict)
        cases = []
        _cases = d.pop("cases", UNSET)
        for cases_item_data in _cases or []:

            def _parse_cases_item(data: object) -> Union["TestCaseType0", None]:
                if data is None:
                    return data
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_test_case_type_0 = TestCaseType0.from_dict(data)

                    return componentsschemas_test_case_type_0
                except:  # noqa: E722
                    pass
                return cast(Union["TestCaseType0", None], data)

            cases_item = _parse_cases_item(cases_item_data)

            cases.append(cases_item)

        list_agent_tests_response_200 = cls(
            cases=cases,
        )

        list_agent_tests_response_200.additional_properties = d
        return list_agent_tests_response_200

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
