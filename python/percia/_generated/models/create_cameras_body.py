from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.create_cameras_body_cameras_item import CreateCamerasBodyCamerasItem


T = TypeVar("T", bound="CreateCamerasBody")


@_attrs_define
class CreateCamerasBody:
    """
    Attributes:
        cameras (list['CreateCamerasBodyCamerasItem']):
    """

    cameras: list["CreateCamerasBodyCamerasItem"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        cameras = []
        for cameras_item_data in self.cameras:
            cameras_item = cameras_item_data.to_dict()
            cameras.append(cameras_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "cameras": cameras,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.create_cameras_body_cameras_item import (
            CreateCamerasBodyCamerasItem,
        )

        d = dict(src_dict)
        cameras = []
        _cameras = d.pop("cameras")
        for cameras_item_data in _cameras:
            cameras_item = CreateCamerasBodyCamerasItem.from_dict(cameras_item_data)

            cameras.append(cameras_item)

        create_cameras_body = cls(
            cameras=cameras,
        )

        create_cameras_body.additional_properties = d
        return create_cameras_body

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
