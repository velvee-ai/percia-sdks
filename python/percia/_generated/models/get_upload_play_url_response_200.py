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

from ..types import UNSET, Unset

T = TypeVar("T", bound="GetUploadPlayUrlResponse200")


@_attrs_define
class GetUploadPlayUrlResponse200:
    """
    Attributes:
        duration_seconds (Union[None, Unset, float]):
        expires_at (Union[Unset, datetime.datetime]):
        has_audio (Union[Unset, bool]):
        url (Union[Unset, str]):
    """

    duration_seconds: Union[None, Unset, float] = UNSET
    expires_at: Union[Unset, datetime.datetime] = UNSET
    has_audio: Union[Unset, bool] = UNSET
    url: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        duration_seconds: Union[None, Unset, float]
        if isinstance(self.duration_seconds, Unset):
            duration_seconds = UNSET
        else:
            duration_seconds = self.duration_seconds

        expires_at: Union[Unset, str] = UNSET
        if not isinstance(self.expires_at, Unset):
            expires_at = self.expires_at.isoformat()

        has_audio = self.has_audio

        url = self.url

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if duration_seconds is not UNSET:
            field_dict["durationSeconds"] = duration_seconds
        if expires_at is not UNSET:
            field_dict["expiresAt"] = expires_at
        if has_audio is not UNSET:
            field_dict["hasAudio"] = has_audio
        if url is not UNSET:
            field_dict["url"] = url

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_duration_seconds(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        duration_seconds = _parse_duration_seconds(d.pop("durationSeconds", UNSET))

        _expires_at = d.pop("expiresAt", UNSET)
        expires_at: Union[Unset, datetime.datetime]
        if isinstance(_expires_at, Unset):
            expires_at = UNSET
        else:
            expires_at = isoparse(_expires_at)

        has_audio = d.pop("hasAudio", UNSET)

        url = d.pop("url", UNSET)

        get_upload_play_url_response_200 = cls(
            duration_seconds=duration_seconds,
            expires_at=expires_at,
            has_audio=has_audio,
            url=url,
        )

        get_upload_play_url_response_200.additional_properties = d
        return get_upload_play_url_response_200

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
