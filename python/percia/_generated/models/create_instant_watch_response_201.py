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
    from ..models.watch import Watch


T = TypeVar("T", bound="CreateInstantWatchResponse201")


@_attrs_define
class CreateInstantWatchResponse201:
    """
    Attributes:
        api_key (Union[Unset, str]):
        claim_url (Union[Unset, str]): Open while signed in to keep the watch.
        expires_at (Union[Unset, datetime.datetime]):
        watch (Union[Unset, Watch]):
        webhook_secret (Union[Unset, str]):
    """

    api_key: Union[Unset, str] = UNSET
    claim_url: Union[Unset, str] = UNSET
    expires_at: Union[Unset, datetime.datetime] = UNSET
    watch: Union[Unset, "Watch"] = UNSET
    webhook_secret: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        api_key = self.api_key

        claim_url = self.claim_url

        expires_at: Union[Unset, str] = UNSET
        if not isinstance(self.expires_at, Unset):
            expires_at = self.expires_at.isoformat()

        watch: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.watch, Unset):
            watch = self.watch.to_dict()

        webhook_secret = self.webhook_secret

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if api_key is not UNSET:
            field_dict["apiKey"] = api_key
        if claim_url is not UNSET:
            field_dict["claimUrl"] = claim_url
        if expires_at is not UNSET:
            field_dict["expiresAt"] = expires_at
        if watch is not UNSET:
            field_dict["watch"] = watch
        if webhook_secret is not UNSET:
            field_dict["webhookSecret"] = webhook_secret

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.watch import Watch

        d = dict(src_dict)
        api_key = d.pop("apiKey", UNSET)

        claim_url = d.pop("claimUrl", UNSET)

        _expires_at = d.pop("expiresAt", UNSET)
        expires_at: Union[Unset, datetime.datetime]
        if isinstance(_expires_at, Unset):
            expires_at = UNSET
        else:
            expires_at = isoparse(_expires_at)

        _watch = d.pop("watch", UNSET)
        watch: Union[Unset, Watch]
        if isinstance(_watch, Unset):
            watch = UNSET
        else:
            watch = Watch.from_dict(_watch)

        webhook_secret = d.pop("webhookSecret", UNSET)

        create_instant_watch_response_201 = cls(
            api_key=api_key,
            claim_url=claim_url,
            expires_at=expires_at,
            watch=watch,
            webhook_secret=webhook_secret,
        )

        create_instant_watch_response_201.additional_properties = d
        return create_instant_watch_response_201

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
