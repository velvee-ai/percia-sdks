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
    from ..models.list_test_runs_response_200_latest_type_0 import (
        ListTestRunsResponse200LatestType0,
    )
    from ..models.list_test_runs_response_200_tests_item import (
        ListTestRunsResponse200TestsItem,
    )


T = TypeVar("T", bound="ListTestRunsResponse200")


@_attrs_define
class ListTestRunsResponse200:
    """
    Attributes:
        latest (Union['ListTestRunsResponse200LatestType0', None, Unset]):
        running (Union[None, Unset, str]):
        tests (Union[Unset, list['ListTestRunsResponse200TestsItem']]):
    """

    latest: Union["ListTestRunsResponse200LatestType0", None, Unset] = UNSET
    running: Union[None, Unset, str] = UNSET
    tests: Union[Unset, list["ListTestRunsResponse200TestsItem"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.list_test_runs_response_200_latest_type_0 import (
            ListTestRunsResponse200LatestType0,
        )

        latest: Union[None, Unset, dict[str, Any]]
        if isinstance(self.latest, Unset):
            latest = UNSET
        elif isinstance(self.latest, ListTestRunsResponse200LatestType0):
            latest = self.latest.to_dict()
        else:
            latest = self.latest

        running: Union[None, Unset, str]
        if isinstance(self.running, Unset):
            running = UNSET
        else:
            running = self.running

        tests: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.tests, Unset):
            tests = []
            for tests_item_data in self.tests:
                tests_item = tests_item_data.to_dict()
                tests.append(tests_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if latest is not UNSET:
            field_dict["latest"] = latest
        if running is not UNSET:
            field_dict["running"] = running
        if tests is not UNSET:
            field_dict["tests"] = tests

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.list_test_runs_response_200_latest_type_0 import (
            ListTestRunsResponse200LatestType0,
        )
        from ..models.list_test_runs_response_200_tests_item import (
            ListTestRunsResponse200TestsItem,
        )

        d = dict(src_dict)

        def _parse_latest(
            data: object,
        ) -> Union["ListTestRunsResponse200LatestType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                latest_type_0 = ListTestRunsResponse200LatestType0.from_dict(data)

                return latest_type_0
            except:  # noqa: E722
                pass
            return cast(Union["ListTestRunsResponse200LatestType0", None, Unset], data)

        latest = _parse_latest(d.pop("latest", UNSET))

        def _parse_running(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        running = _parse_running(d.pop("running", UNSET))

        tests = []
        _tests = d.pop("tests", UNSET)
        for tests_item_data in _tests or []:
            tests_item = ListTestRunsResponse200TestsItem.from_dict(tests_item_data)

            tests.append(tests_item)

        list_test_runs_response_200 = cls(
            latest=latest,
            running=running,
            tests=tests,
        )

        list_test_runs_response_200.additional_properties = d
        return list_test_runs_response_200

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
