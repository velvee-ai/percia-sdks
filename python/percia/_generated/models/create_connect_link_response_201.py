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

T = TypeVar("T", bound="CreateConnectLinkResponse201")


@_attrs_define
class CreateConnectLinkResponse201:
    """
    Attributes:
        connect_url (Union[Unset, str]): Single-use link (15 minutes) for the person to open while signed in to Percia;
            you cannot open or finish it for them. Show it (with MCP, with the show_link tool), ask them to say when they
            are done, then check GET /integrations once. Do not poll. A new connection to the destination of a broken one
            replaces it and takes over its rules.
        expires_at (Union[Unset, datetime.datetime]):
    """

    connect_url: Union[Unset, str] = UNSET
    expires_at: Union[Unset, datetime.datetime] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        connect_url = self.connect_url

        expires_at: Union[Unset, str] = UNSET
        if not isinstance(self.expires_at, Unset):
            expires_at = self.expires_at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if connect_url is not UNSET:
            field_dict["connectUrl"] = connect_url
        if expires_at is not UNSET:
            field_dict["expiresAt"] = expires_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        connect_url = d.pop("connectUrl", UNSET)

        _expires_at = d.pop("expiresAt", UNSET)
        expires_at: Union[Unset, datetime.datetime]
        if isinstance(_expires_at, Unset):
            expires_at = UNSET
        else:
            expires_at = isoparse(_expires_at)

        create_connect_link_response_201 = cls(
            connect_url=connect_url,
            expires_at=expires_at,
        )

        create_connect_link_response_201.additional_properties = d
        return create_connect_link_response_201

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
