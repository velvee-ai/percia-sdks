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
    from ..models.metric import Metric


T = TypeVar("T", bound="GetMetricsResponse200")


@_attrs_define
class GetMetricsResponse200:
    """
    Attributes:
        agents (Union[Unset, list['Metric']]):
        days (Union[Unset, int]):
        watches (Union[Unset, list['Metric']]):
    """

    agents: Union[Unset, list["Metric"]] = UNSET
    days: Union[Unset, int] = UNSET
    watches: Union[Unset, list["Metric"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        agents: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.agents, Unset):
            agents = []
            for agents_item_data in self.agents:
                agents_item = agents_item_data.to_dict()
                agents.append(agents_item)

        days = self.days

        watches: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.watches, Unset):
            watches = []
            for watches_item_data in self.watches:
                watches_item = watches_item_data.to_dict()
                watches.append(watches_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if agents is not UNSET:
            field_dict["agents"] = agents
        if days is not UNSET:
            field_dict["days"] = days
        if watches is not UNSET:
            field_dict["watches"] = watches

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.metric import Metric

        d = dict(src_dict)
        agents = []
        _agents = d.pop("agents", UNSET)
        for agents_item_data in _agents or []:
            agents_item = Metric.from_dict(agents_item_data)

            agents.append(agents_item)

        days = d.pop("days", UNSET)

        watches = []
        _watches = d.pop("watches", UNSET)
        for watches_item_data in _watches or []:
            watches_item = Metric.from_dict(watches_item_data)

            watches.append(watches_item)

        get_metrics_response_200 = cls(
            agents=agents,
            days=days,
            watches=watches,
        )

        get_metrics_response_200.additional_properties = d
        return get_metrics_response_200

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
