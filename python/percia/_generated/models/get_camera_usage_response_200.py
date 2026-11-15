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
    from ..models.get_camera_usage_response_200_cameras_item import (
        GetCameraUsageResponse200CamerasItem,
    )


T = TypeVar("T", bound="GetCameraUsageResponse200")


@_attrs_define
class GetCameraUsageResponse200:
    """
    Attributes:
        cameras (Union[Unset, list['GetCameraUsageResponse200CamerasItem']]):
        cents_per_camera_hour (Union[Unset, int]):
        month (Union[Unset, str]): YYYY-MM (UTC).
        total_cost_cents (Union[Unset, int]):
        total_minutes (Union[Unset, int]):
        unattributed_minutes (Union[Unset, int]):
    """

    cameras: Union[Unset, list["GetCameraUsageResponse200CamerasItem"]] = UNSET
    cents_per_camera_hour: Union[Unset, int] = UNSET
    month: Union[Unset, str] = UNSET
    total_cost_cents: Union[Unset, int] = UNSET
    total_minutes: Union[Unset, int] = UNSET
    unattributed_minutes: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        cameras: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.cameras, Unset):
            cameras = []
            for cameras_item_data in self.cameras:
                cameras_item = cameras_item_data.to_dict()
                cameras.append(cameras_item)

        cents_per_camera_hour = self.cents_per_camera_hour

        month = self.month

        total_cost_cents = self.total_cost_cents

        total_minutes = self.total_minutes

        unattributed_minutes = self.unattributed_minutes

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if cameras is not UNSET:
            field_dict["cameras"] = cameras
        if cents_per_camera_hour is not UNSET:
            field_dict["centsPerCameraHour"] = cents_per_camera_hour
        if month is not UNSET:
            field_dict["month"] = month
        if total_cost_cents is not UNSET:
            field_dict["totalCostCents"] = total_cost_cents
        if total_minutes is not UNSET:
            field_dict["totalMinutes"] = total_minutes
        if unattributed_minutes is not UNSET:
            field_dict["unattributedMinutes"] = unattributed_minutes

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.get_camera_usage_response_200_cameras_item import (
            GetCameraUsageResponse200CamerasItem,
        )

        d = dict(src_dict)
        cameras = []
        _cameras = d.pop("cameras", UNSET)
        for cameras_item_data in _cameras or []:
            cameras_item = GetCameraUsageResponse200CamerasItem.from_dict(cameras_item_data)

            cameras.append(cameras_item)

        cents_per_camera_hour = d.pop("centsPerCameraHour", UNSET)

        month = d.pop("month", UNSET)

        total_cost_cents = d.pop("totalCostCents", UNSET)

        total_minutes = d.pop("totalMinutes", UNSET)

        unattributed_minutes = d.pop("unattributedMinutes", UNSET)

        get_camera_usage_response_200 = cls(
            cameras=cameras,
            cents_per_camera_hour=cents_per_camera_hour,
            month=month,
            total_cost_cents=total_cost_cents,
            total_minutes=total_minutes,
            unattributed_minutes=unattributed_minutes,
        )

        get_camera_usage_response_200.additional_properties = d
        return get_camera_usage_response_200

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
