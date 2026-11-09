import datetime
from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.camera import Camera


T = TypeVar("T", bound="CreateCameraResponse201")


@_attrs_define
class CreateCameraResponse201:
    """
    Attributes:
        camera (Union[Unset, Camera]):
        pair_expires_at (Union[Unset, datetime.datetime]):
        pair_url (Union[Unset, str]): Single-use link (10 minutes) for the person to open on the phone that will be the
            camera; you cannot open it for them. On an iPhone with the Percia Camera app it pairs in the app, otherwise the
            page can pair the browser. Tell them to keep the app or page open on screen while it watches: the camera stops
            when they switch apps or lock the phone, so they should keep talking to you from another device. With MCP, show
            it with the show_link tool.
    """

    camera: Union[Unset, "Camera"] = UNSET
    pair_expires_at: Union[Unset, datetime.datetime] = UNSET
    pair_url: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        camera: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.camera, Unset):
            camera = self.camera.to_dict()

        pair_expires_at: Union[Unset, str] = UNSET
        if not isinstance(self.pair_expires_at, Unset):
            pair_expires_at = self.pair_expires_at.isoformat()

        pair_url = self.pair_url

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if camera is not UNSET:
            field_dict["camera"] = camera
        if pair_expires_at is not UNSET:
            field_dict["pairExpiresAt"] = pair_expires_at
        if pair_url is not UNSET:
            field_dict["pairUrl"] = pair_url

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

        _pair_expires_at = d.pop("pairExpiresAt", UNSET)
        pair_expires_at: Union[Unset, datetime.datetime]
        if isinstance(_pair_expires_at, Unset):
            pair_expires_at = UNSET
        else:
            pair_expires_at = isoparse(_pair_expires_at)

        pair_url = d.pop("pairUrl", UNSET)

        create_camera_response_201 = cls(
            camera=camera,
            pair_expires_at=pair_expires_at,
            pair_url=pair_url,
        )

        create_camera_response_201.additional_properties = d
        return create_camera_response_201

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
