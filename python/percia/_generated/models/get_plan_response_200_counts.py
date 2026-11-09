from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="GetPlanResponse200Counts")


@_attrs_define
class GetPlanResponse200Counts:
    """
    Attributes:
        active_watches (Union[Unset, int]):
        agents (Union[Unset, int]):
        phone_cameras (Union[Unset, int]):
    """

    active_watches: Union[Unset, int] = UNSET
    agents: Union[Unset, int] = UNSET
    phone_cameras: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        active_watches = self.active_watches

        agents = self.agents

        phone_cameras = self.phone_cameras

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if active_watches is not UNSET:
            field_dict["activeWatches"] = active_watches
        if agents is not UNSET:
            field_dict["agents"] = agents
        if phone_cameras is not UNSET:
            field_dict["phoneCameras"] = phone_cameras

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        active_watches = d.pop("activeWatches", UNSET)

        agents = d.pop("agents", UNSET)

        phone_cameras = d.pop("phoneCameras", UNSET)

        get_plan_response_200_counts = cls(
            active_watches=active_watches,
            agents=agents,
            phone_cameras=phone_cameras,
        )

        get_plan_response_200_counts.additional_properties = d
        return get_plan_response_200_counts

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
