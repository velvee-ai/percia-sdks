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
    from ..models.create_cameras_response_201_cameras_item import (
        CreateCamerasResponse201CamerasItem,
    )


T = TypeVar("T", bound="CreateCamerasResponse201")


@_attrs_define
class CreateCamerasResponse201:
    """
    Attributes:
        cameras (Union[Unset, list['CreateCamerasResponse201CamerasItem']]):
    """

    cameras: Union[Unset, list["CreateCamerasResponse201CamerasItem"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        cameras: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.cameras, Unset):
            cameras = []
            for cameras_item_data in self.cameras:
                cameras_item = cameras_item_data.to_dict()
                cameras.append(cameras_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if cameras is not UNSET:
            field_dict["cameras"] = cameras

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.create_cameras_response_201_cameras_item import (
            CreateCamerasResponse201CamerasItem,
        )

        d = dict(src_dict)
        cameras = []
        _cameras = d.pop("cameras", UNSET)
        for cameras_item_data in _cameras or []:
            cameras_item = CreateCamerasResponse201CamerasItem.from_dict(cameras_item_data)

            cameras.append(cameras_item)

        create_cameras_response_201 = cls(
            cameras=cameras,
        )

        create_cameras_response_201.additional_properties = d
        return create_cameras_response_201

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
