import datetime
from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateUploadLinkResponse201")


@_attrs_define
class CreateUploadLinkResponse201:
    """
    Attributes:
        created_at (Union[Unset, datetime.datetime]):
        expires_at (Union[Unset, datetime.datetime]):
        max_mb (Union[Unset, int]):
        max_seconds (Union[Unset, int]):
        next_ (Union[Unset, str]):
        upload_url (Union[Unset, str]):
    """

    created_at: Union[Unset, datetime.datetime] = UNSET
    expires_at: Union[Unset, datetime.datetime] = UNSET
    max_mb: Union[Unset, int] = UNSET
    max_seconds: Union[Unset, int] = UNSET
    next_: Union[Unset, str] = UNSET
    upload_url: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        created_at: Union[Unset, str] = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()

        expires_at: Union[Unset, str] = UNSET
        if not isinstance(self.expires_at, Unset):
            expires_at = self.expires_at.isoformat()

        max_mb = self.max_mb

        max_seconds = self.max_seconds

        next_ = self.next_

        upload_url = self.upload_url

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if created_at is not UNSET:
            field_dict["createdAt"] = created_at
        if expires_at is not UNSET:
            field_dict["expiresAt"] = expires_at
        if max_mb is not UNSET:
            field_dict["maxMb"] = max_mb
        if max_seconds is not UNSET:
            field_dict["maxSeconds"] = max_seconds
        if next_ is not UNSET:
            field_dict["next"] = next_
        if upload_url is not UNSET:
            field_dict["uploadUrl"] = upload_url

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _created_at = d.pop("createdAt", UNSET)
        created_at: Union[Unset, datetime.datetime]
        if isinstance(_created_at, Unset):
            created_at = UNSET
        else:
            created_at = isoparse(_created_at)

        _expires_at = d.pop("expiresAt", UNSET)
        expires_at: Union[Unset, datetime.datetime]
        if isinstance(_expires_at, Unset):
            expires_at = UNSET
        else:
            expires_at = isoparse(_expires_at)

        max_mb = d.pop("maxMb", UNSET)

        max_seconds = d.pop("maxSeconds", UNSET)

        next_ = d.pop("next", UNSET)

        upload_url = d.pop("uploadUrl", UNSET)

        create_upload_link_response_201 = cls(
            created_at=created_at,
            expires_at=expires_at,
            max_mb=max_mb,
            max_seconds=max_seconds,
            next_=next_,
            upload_url=upload_url,
        )

        create_upload_link_response_201.additional_properties = d
        return create_upload_link_response_201

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
