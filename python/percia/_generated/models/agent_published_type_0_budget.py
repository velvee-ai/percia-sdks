from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="AgentPublishedType0Budget")


@_attrs_define
class AgentPublishedType0Budget:
    """
    Attributes:
        max_requests_per_min (Union[Unset, int]):  Default: 6.
    """

    max_requests_per_min: Union[Unset, int] = 6
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        max_requests_per_min = self.max_requests_per_min

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if max_requests_per_min is not UNSET:
            field_dict["maxRequestsPerMin"] = max_requests_per_min

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        max_requests_per_min = d.pop("maxRequestsPerMin", UNSET)

        agent_published_type_0_budget = cls(
            max_requests_per_min=max_requests_per_min,
        )

        agent_published_type_0_budget.additional_properties = d
        return agent_published_type_0_budget

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
