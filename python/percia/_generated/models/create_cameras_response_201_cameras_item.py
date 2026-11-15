from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
    Union,
    cast,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.camera import Camera


T = TypeVar("T", bound="CreateCamerasResponse201CamerasItem")


@_attrs_define
class CreateCamerasResponse201CamerasItem:
    """
    Attributes:
        camera (Union[Unset, Camera]):
        existing (Union[Unset, bool]):
        token (Union[None, Unset, str]):
        whip_url (Union[Unset, str]):
    """

    camera: Union[Unset, "Camera"] = UNSET
    existing: Union[Unset, bool] = UNSET
    token: Union[None, Unset, str] = UNSET
    whip_url: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        camera: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.camera, Unset):
            camera = self.camera.to_dict()

        existing = self.existing

        token: Union[None, Unset, str]
        if isinstance(self.token, Unset):
            token = UNSET
        else:
            token = self.token

        whip_url = self.whip_url

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if camera is not UNSET:
            field_dict["camera"] = camera
        if existing is not UNSET:
            field_dict["existing"] = existing
        if token is not UNSET:
            field_dict["token"] = token
        if whip_url is not UNSET:
            field_dict["whipUrl"] = whip_url

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.camera import Camera

        d = dict(src_dict)
        _camera = d.pop("camera", UNSET)
        camera: Union[Unset, Camera]
        if isinstance(_camera, Unset):
            camera = UNSET
        else:
            camera = Camera.from_dict(_camera)

        existing = d.pop("existing", UNSET)

        def _parse_token(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        token = _parse_token(d.pop("token", UNSET))

        whip_url = d.pop("whipUrl", UNSET)

        create_cameras_response_201_cameras_item = cls(
            camera=camera,
            existing=existing,
            token=token,
            whip_url=whip_url,
        )

        create_cameras_response_201_cameras_item.additional_properties = d
        return create_cameras_response_201_cameras_item

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
