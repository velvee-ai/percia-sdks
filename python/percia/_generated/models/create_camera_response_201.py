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
    from ..models.create_camera_response_201_publish import (
        CreateCameraResponse201Publish,
    )


T = TypeVar("T", bound="CreateCameraResponse201")


@_attrs_define
class CreateCameraResponse201:
    """
    Attributes:
        camera (Union[Unset, Camera]):
        expires_at (Union[Unset, None]):
        pair_expires_at (Union[Unset, datetime.datetime]):
        pair_url (Union[Unset, str]): Single-use link (10 minutes) for the person to open on the phone, tablet or
            computer that will be the camera (also for "use my laptop/webcam as a camera"); you cannot open it for them. On
            an iPhone with the Percia Camera app it pairs in the app, otherwise the page can pair the browser. Tell them to
            keep the app or page open on screen while it watches: the camera stops when they switch apps or lock the device,
            so they should keep talking to you from another device. With MCP, show it with the show_link tool.
        publish (Union[Unset, CreateCameraResponse201Publish]):
        token (Union[Unset, str]): Publish token for this one camera (pc_...), shown once. Publish only; never read.
        whip_url (Union[Unset, str]):
    """

    camera: Union[Unset, "Camera"] = UNSET
    expires_at: Union[Unset, None] = UNSET
    pair_expires_at: Union[Unset, datetime.datetime] = UNSET
    pair_url: Union[Unset, str] = UNSET
    publish: Union[Unset, "CreateCameraResponse201Publish"] = UNSET
    token: Union[Unset, str] = UNSET
    whip_url: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        camera: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.camera, Unset):
            camera = self.camera.to_dict()

        expires_at = self.expires_at

        pair_expires_at: Union[Unset, str] = UNSET
        if not isinstance(self.pair_expires_at, Unset):
            pair_expires_at = self.pair_expires_at.isoformat()

        pair_url = self.pair_url

        publish: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.publish, Unset):
            publish = self.publish.to_dict()

        token = self.token

        whip_url = self.whip_url

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if camera is not UNSET:
            field_dict["camera"] = camera
        if expires_at is not UNSET:
            field_dict["expiresAt"] = expires_at
        if pair_expires_at is not UNSET:
            field_dict["pairExpiresAt"] = pair_expires_at
        if pair_url is not UNSET:
            field_dict["pairUrl"] = pair_url
        if publish is not UNSET:
            field_dict["publish"] = publish
        if token is not UNSET:
            field_dict["token"] = token
        if whip_url is not UNSET:
            field_dict["whipUrl"] = whip_url

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.camera import Camera
        from ..models.create_camera_response_201_publish import (
            CreateCameraResponse201Publish,
        )

        d = dict(src_dict)
        _camera = d.pop("camera", UNSET)
        camera: Union[Unset, Camera]
        if isinstance(_camera, Unset):
            camera = UNSET
        else:
            camera = Camera.from_dict(_camera)

        expires_at = d.pop("expiresAt", UNSET)

        _pair_expires_at = d.pop("pairExpiresAt", UNSET)
        pair_expires_at: Union[Unset, datetime.datetime]
        if isinstance(_pair_expires_at, Unset):
            pair_expires_at = UNSET
        else:
            pair_expires_at = isoparse(_pair_expires_at)

        pair_url = d.pop("pairUrl", UNSET)

        _publish = d.pop("publish", UNSET)
        publish: Union[Unset, CreateCameraResponse201Publish]
        if isinstance(_publish, Unset):
            publish = UNSET
        else:
            publish = CreateCameraResponse201Publish.from_dict(_publish)

        token = d.pop("token", UNSET)

        whip_url = d.pop("whipUrl", UNSET)

        create_camera_response_201 = cls(
            camera=camera,
            expires_at=expires_at,
            pair_expires_at=pair_expires_at,
            pair_url=pair_url,
            publish=publish,
            token=token,
            whip_url=whip_url,
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
