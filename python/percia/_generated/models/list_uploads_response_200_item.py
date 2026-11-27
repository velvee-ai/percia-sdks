import datetime
from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
    cast,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.list_uploads_response_200_item_codec_type_1 import (
    ListUploadsResponse200ItemCodecType1,
)
from ..models.list_uploads_response_200_item_container_type_1 import (
    ListUploadsResponse200ItemContainerType1,
)
from ..models.list_uploads_response_200_item_status import (
    ListUploadsResponse200ItemStatus,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="ListUploadsResponse200Item")


@_attrs_define
class ListUploadsResponse200Item:
    """
    Attributes:
        codec (Union[ListUploadsResponse200ItemCodecType1, None, Unset]):
        container (Union[ListUploadsResponse200ItemContainerType1, None, Unset]):
        created_at (Union[Unset, datetime.datetime]):
        duration_seconds (Union[None, Unset, float]):
        error (Union[None, Unset, str]): Why a `failed` upload was refused.
        expires_at (Union[Unset, datetime.datetime]): The file is deleted then, or earlier with its last watch.
        has_audio (Union[Unset, bool]): The audio is never used: the watch reads video only and the player is muted.
        height (Union[None, Unset, int]):
        id (Union[Unset, str]):
        name (Union[Unset, str]):
        size (Union[Unset, int]): Bytes.
        source (Union[Unset, str]): Use as `sourceUrl` of POST /watches: percia-file://<id>. Append ?loop=1 to repeat
            the file (testing; only where looping is enabled).
        status (Union[Unset, ListUploadsResponse200ItemStatus]): Only `ready` files can be a watch source.
        width (Union[None, Unset, int]):
    """

    codec: Union[ListUploadsResponse200ItemCodecType1, None, Unset] = UNSET
    container: Union[ListUploadsResponse200ItemContainerType1, None, Unset] = UNSET
    created_at: Union[Unset, datetime.datetime] = UNSET
    duration_seconds: Union[None, Unset, float] = UNSET
    error: Union[None, Unset, str] = UNSET
    expires_at: Union[Unset, datetime.datetime] = UNSET
    has_audio: Union[Unset, bool] = UNSET
    height: Union[None, Unset, int] = UNSET
    id: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    size: Union[Unset, int] = UNSET
    source: Union[Unset, str] = UNSET
    status: Union[Unset, ListUploadsResponse200ItemStatus] = UNSET
    width: Union[None, Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        codec: Union[None, Unset, str]
        if isinstance(self.codec, Unset):
            codec = UNSET
        elif isinstance(self.codec, ListUploadsResponse200ItemCodecType1):
            codec = self.codec.value
        else:
            codec = self.codec

        container: Union[None, Unset, str]
        if isinstance(self.container, Unset):
            container = UNSET
        elif isinstance(self.container, ListUploadsResponse200ItemContainerType1):
            container = self.container.value
        else:
            container = self.container

        created_at: Union[Unset, str] = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()

        duration_seconds: Union[None, Unset, float]
        if isinstance(self.duration_seconds, Unset):
            duration_seconds = UNSET
        else:
            duration_seconds = self.duration_seconds

        error: Union[None, Unset, str]
        if isinstance(self.error, Unset):
            error = UNSET
        else:
            error = self.error

        expires_at: Union[Unset, str] = UNSET
        if not isinstance(self.expires_at, Unset):
            expires_at = self.expires_at.isoformat()

        has_audio = self.has_audio

        height: Union[None, Unset, int]
        if isinstance(self.height, Unset):
            height = UNSET
        else:
            height = self.height

        id = self.id

        name = self.name

        size = self.size

        source = self.source

        status: Union[Unset, str] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        width: Union[None, Unset, int]
        if isinstance(self.width, Unset):
            width = UNSET
        else:
            width = self.width

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if codec is not UNSET:
            field_dict["codec"] = codec
        if container is not UNSET:
            field_dict["container"] = container
        if created_at is not UNSET:
            field_dict["createdAt"] = created_at
        if duration_seconds is not UNSET:
            field_dict["durationSeconds"] = duration_seconds
        if error is not UNSET:
            field_dict["error"] = error
        if expires_at is not UNSET:
            field_dict["expiresAt"] = expires_at
        if has_audio is not UNSET:
            field_dict["hasAudio"] = has_audio
        if height is not UNSET:
            field_dict["height"] = height
        if id is not UNSET:
            field_dict["id"] = id
        if name is not UNSET:
            field_dict["name"] = name
        if size is not UNSET:
            field_dict["size"] = size
        if source is not UNSET:
            field_dict["source"] = source
        if status is not UNSET:
            field_dict["status"] = status
        if width is not UNSET:
            field_dict["width"] = width

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_codec(
            data: object,
        ) -> Union[ListUploadsResponse200ItemCodecType1, None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                codec_type_1 = ListUploadsResponse200ItemCodecType1(data)

                return codec_type_1
            except:  # noqa: E722
                pass
            return cast(Union[ListUploadsResponse200ItemCodecType1, None, Unset], data)

        codec = _parse_codec(d.pop("codec", UNSET))

        def _parse_container(
            data: object,
        ) -> Union[ListUploadsResponse200ItemContainerType1, None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                container_type_1 = ListUploadsResponse200ItemContainerType1(data)

                return container_type_1
            except:  # noqa: E722
                pass
            return cast(Union[ListUploadsResponse200ItemContainerType1, None, Unset], data)

        container = _parse_container(d.pop("container", UNSET))

        _created_at = d.pop("createdAt", UNSET)
        created_at: Union[Unset, datetime.datetime]
        if isinstance(_created_at, Unset):
            created_at = UNSET
        else:
            created_at = isoparse(_created_at)

        def _parse_duration_seconds(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        duration_seconds = _parse_duration_seconds(d.pop("durationSeconds", UNSET))

        def _parse_error(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        error = _parse_error(d.pop("error", UNSET))

        _expires_at = d.pop("expiresAt", UNSET)
        expires_at: Union[Unset, datetime.datetime]
        if isinstance(_expires_at, Unset):
            expires_at = UNSET
        else:
            expires_at = isoparse(_expires_at)

        has_audio = d.pop("hasAudio", UNSET)

        def _parse_height(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        height = _parse_height(d.pop("height", UNSET))

        id = d.pop("id", UNSET)

        name = d.pop("name", UNSET)

        size = d.pop("size", UNSET)

        source = d.pop("source", UNSET)

        _status = d.pop("status", UNSET)
        status: Union[Unset, ListUploadsResponse200ItemStatus]
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = ListUploadsResponse200ItemStatus(_status)

        def _parse_width(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        width = _parse_width(d.pop("width", UNSET))

        list_uploads_response_200_item = cls(
            codec=codec,
            container=container,
            created_at=created_at,
            duration_seconds=duration_seconds,
            error=error,
            expires_at=expires_at,
            has_audio=has_audio,
            height=height,
            id=id,
            name=name,
            size=size,
            source=source,
            status=status,
            width=width,
        )

        list_uploads_response_200_item.additional_properties = d
        return list_uploads_response_200_item

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
