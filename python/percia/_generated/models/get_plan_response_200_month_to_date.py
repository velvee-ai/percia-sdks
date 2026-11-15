from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="GetPlanResponse200MonthToDate")


@_attrs_define
class GetPlanResponse200MonthToDate:
    """
    Attributes:
        camera_minutes (Union[Unset, int]):
        cents (Union[Unset, int]):
    """

    camera_minutes: Union[Unset, int] = UNSET
    cents: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        camera_minutes = self.camera_minutes

        cents = self.cents

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if camera_minutes is not UNSET:
            field_dict["cameraMinutes"] = camera_minutes
        if cents is not UNSET:
            field_dict["cents"] = cents

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        camera_minutes = d.pop("cameraMinutes", UNSET)

        cents = d.pop("cents", UNSET)

        get_plan_response_200_month_to_date = cls(
            camera_minutes=camera_minutes,
            cents=cents,
        )

        get_plan_response_200_month_to_date.additional_properties = d
        return get_plan_response_200_month_to_date

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
