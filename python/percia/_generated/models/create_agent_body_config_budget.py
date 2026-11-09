from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateAgentBodyConfigBudget")


@_attrs_define
class CreateAgentBodyConfigBudget:
    """
    Attributes:
        max_requests_per_min (Union[Unset, int]):  Default: 6.
    """

    max_requests_per_min: Union[Unset, int] = 6

    def to_dict(self) -> dict[str, Any]:
        max_requests_per_min = self.max_requests_per_min

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if max_requests_per_min is not UNSET:
            field_dict["maxRequestsPerMin"] = max_requests_per_min

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        max_requests_per_min = d.pop("maxRequestsPerMin", UNSET)

        create_agent_body_config_budget = cls(
            max_requests_per_min=max_requests_per_min,
        )

        return create_agent_body_config_budget
