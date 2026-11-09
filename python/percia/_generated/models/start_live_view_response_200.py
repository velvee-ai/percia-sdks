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

T = TypeVar("T", bound="StartLiveViewResponse200")


@_attrs_define
class StartLiveViewResponse200:
    """
    Attributes:
        expires_at (Union[Unset, datetime.datetime]):
        latest_keyframe (Union[None, Unset, str]):
        latest_keyframe_at (Union[None, Unset, datetime.datetime]):
        token (Union[Unset, str]):
        whep_url (Union[Unset, str]):
    """

    expires_at: Union[Unset, datetime.datetime] = UNSET
    latest_keyframe: Union[None, Unset, str] = UNSET
    latest_keyframe_at: Union[None, Unset, datetime.datetime] = UNSET
    token: Union[Unset, str] = UNSET
    whep_url: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        expires_at: Union[Unset, str] = UNSET
        if not isinstance(self.expires_at, Unset):
            expires_at = self.expires_at.isoformat()

        latest_keyframe: Union[None, Unset, str]
        if isinstance(self.latest_keyframe, Unset):
            latest_keyframe = UNSET
        else:
            latest_keyframe = self.latest_keyframe

        latest_keyframe_at: Union[None, Unset, str]
        if isinstance(self.latest_keyframe_at, Unset):
            latest_keyframe_at = UNSET
        elif isinstance(self.latest_keyframe_at, datetime.datetime):
            latest_keyframe_at = self.latest_keyframe_at.isoformat()
        else:
            latest_keyframe_at = self.latest_keyframe_at

        token = self.token

        whep_url = self.whep_url

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if expires_at is not UNSET:
            field_dict["expiresAt"] = expires_at
        if latest_keyframe is not UNSET:
            field_dict["latestKeyframe"] = latest_keyframe
        if latest_keyframe_at is not UNSET:
            field_dict["latestKeyframeAt"] = latest_keyframe_at
        if token is not UNSET:
            field_dict["token"] = token
        if whep_url is not UNSET:
            field_dict["whepUrl"] = whep_url

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _expires_at = d.pop("expiresAt", UNSET)
        expires_at: Union[Unset, datetime.datetime]
        if isinstance(_expires_at, Unset):
            expires_at = UNSET
        else:
            expires_at = isoparse(_expires_at)

        def _parse_latest_keyframe(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        latest_keyframe = _parse_latest_keyframe(d.pop("latestKeyframe", UNSET))

        def _parse_latest_keyframe_at(
            data: object,
        ) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                latest_keyframe_at_type_0 = isoparse(data)

                return latest_keyframe_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        latest_keyframe_at = _parse_latest_keyframe_at(d.pop("latestKeyframeAt", UNSET))

        token = d.pop("token", UNSET)

        whep_url = d.pop("whepUrl", UNSET)

        start_live_view_response_200 = cls(
            expires_at=expires_at,
            latest_keyframe=latest_keyframe,
            latest_keyframe_at=latest_keyframe_at,
            token=token,
            whep_url=whep_url,
        )

        start_live_view_response_200.additional_properties = d
        return start_live_view_response_200

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
