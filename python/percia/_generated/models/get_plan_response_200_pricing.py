from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="GetPlanResponse200Pricing")


@_attrs_define
class GetPlanResponse200Pricing:
    """
    Attributes:
        cents_per_camera_hour (Union[Unset, int]):
        watches_per_stream (Union[Unset, int]):
    """

    cents_per_camera_hour: Union[Unset, int] = UNSET
    watches_per_stream: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        cents_per_camera_hour = self.cents_per_camera_hour

        watches_per_stream = self.watches_per_stream

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if cents_per_camera_hour is not UNSET:
            field_dict["centsPerCameraHour"] = cents_per_camera_hour
        if watches_per_stream is not UNSET:
            field_dict["watchesPerStream"] = watches_per_stream

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        cents_per_camera_hour = d.pop("centsPerCameraHour", UNSET)

        watches_per_stream = d.pop("watchesPerStream", UNSET)

        get_plan_response_200_pricing = cls(
            cents_per_camera_hour=cents_per_camera_hour,
            watches_per_stream=watches_per_stream,
        )

        get_plan_response_200_pricing.additional_properties = d
        return get_plan_response_200_pricing

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
