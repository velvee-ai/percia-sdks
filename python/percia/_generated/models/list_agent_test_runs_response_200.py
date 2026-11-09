from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.test_run import TestRun


T = TypeVar("T", bound="ListAgentTestRunsResponse200")


@_attrs_define
class ListAgentTestRunsResponse200:
    """
    Attributes:
        runs (Union[Unset, list['TestRun']]):
    """

    runs: Union[Unset, list["TestRun"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        runs: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.runs, Unset):
            runs = []
            for runs_item_data in self.runs:
                runs_item = runs_item_data.to_dict()
                runs.append(runs_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if runs is not UNSET:
            field_dict["runs"] = runs

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.test_run import TestRun

        d = dict(src_dict)
        runs = []
        _runs = d.pop("runs", UNSET)
        for runs_item_data in _runs or []:
            runs_item = TestRun.from_dict(runs_item_data)

            runs.append(runs_item)

        list_agent_test_runs_response_200 = cls(
            runs=runs,
        )

        list_agent_test_runs_response_200.additional_properties = d
        return list_agent_test_runs_response_200

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
