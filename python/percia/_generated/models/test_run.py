import datetime
from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    Literal,
    TypeVar,
    Union,
    cast,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.test_run_results_item import TestRunResultsItem


T = TypeVar("T", bound="TestRun")


@_attrs_define
class TestRun:
    """
    Attributes:
        agent_id (Union[Unset, str]):
        created_at (Union[Unset, datetime.datetime]):
        failed (Union[Unset, int]):
        id (Union[Unset, str]):
        pass_rate (Union[None, Unset, float]):
        passed (Union[Unset, int]):
        results (Union[Unset, list['TestRunResultsItem']]):
        total (Union[Unset, int]): Judged cases; skipped ones do not count.
        version (Union[Literal['draft'], Unset, int]): A published version number, or "draft".
    """

    agent_id: Union[Unset, str] = UNSET
    created_at: Union[Unset, datetime.datetime] = UNSET
    failed: Union[Unset, int] = UNSET
    id: Union[Unset, str] = UNSET
    pass_rate: Union[None, Unset, float] = UNSET
    passed: Union[Unset, int] = UNSET
    results: Union[Unset, list["TestRunResultsItem"]] = UNSET
    total: Union[Unset, int] = UNSET
    version: Union[Literal["draft"], Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        agent_id = self.agent_id

        created_at: Union[Unset, str] = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()

        failed = self.failed

        id = self.id

        pass_rate: Union[None, Unset, float]
        if isinstance(self.pass_rate, Unset):
            pass_rate = UNSET
        else:
            pass_rate = self.pass_rate

        passed = self.passed

        results: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.results, Unset):
            results = []
            for results_item_data in self.results:
                results_item = results_item_data.to_dict()
                results.append(results_item)

        total = self.total

        version: Union[Literal["draft"], Unset, int]
        if isinstance(self.version, Unset):
            version = UNSET
        else:
            version = self.version

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if agent_id is not UNSET:
            field_dict["agentId"] = agent_id
        if created_at is not UNSET:
            field_dict["createdAt"] = created_at
        if failed is not UNSET:
            field_dict["failed"] = failed
        if id is not UNSET:
            field_dict["id"] = id
        if pass_rate is not UNSET:
            field_dict["passRate"] = pass_rate
        if passed is not UNSET:
            field_dict["passed"] = passed
        if results is not UNSET:
            field_dict["results"] = results
        if total is not UNSET:
            field_dict["total"] = total
        if version is not UNSET:
            field_dict["version"] = version

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.test_run_results_item import TestRunResultsItem

        d = dict(src_dict)
        agent_id = d.pop("agentId", UNSET)

        _created_at = d.pop("createdAt", UNSET)
        created_at: Union[Unset, datetime.datetime]
        if isinstance(_created_at, Unset):
            created_at = UNSET
        else:
            created_at = isoparse(_created_at)

        failed = d.pop("failed", UNSET)

        id = d.pop("id", UNSET)

        def _parse_pass_rate(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        pass_rate = _parse_pass_rate(d.pop("passRate", UNSET))

        passed = d.pop("passed", UNSET)

        results = []
        _results = d.pop("results", UNSET)
        for results_item_data in _results or []:
            results_item = TestRunResultsItem.from_dict(results_item_data)

            results.append(results_item)

        total = d.pop("total", UNSET)

        def _parse_version(data: object) -> Union[Literal["draft"], Unset, int]:
            if isinstance(data, Unset):
                return data
            version_type_1 = cast(Literal["draft"], data)
            if version_type_1 != "draft":
                raise ValueError(f"version_type_1 must match const 'draft', got '{version_type_1}'")
            return version_type_1
            return cast(Union[Literal["draft"], Unset, int], data)

        version = _parse_version(d.pop("version", UNSET))

        test_run = cls(
            agent_id=agent_id,
            created_at=created_at,
            failed=failed,
            id=id,
            pass_rate=pass_rate,
            passed=passed,
            results=results,
            total=total,
            version=version,
        )

        test_run.additional_properties = d
        return test_run

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
