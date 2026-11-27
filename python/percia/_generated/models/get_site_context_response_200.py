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
    from ..models.get_site_context_response_200_context import (
        GetSiteContextResponse200Context,
    )
    from ..models.get_site_context_response_200_open_requests_item import (
        GetSiteContextResponse200OpenRequestsItem,
    )


T = TypeVar("T", bound="GetSiteContextResponse200")


@_attrs_define
class GetSiteContextResponse200:
    """
    Attributes:
        context (GetSiteContextResponse200Context): The SiteContext with tenant_id, site_id, revision and updated_at set
            by the server.
        revision (int):
        changed (Union[Unset, bool]):
        open_requests (Union[Unset, list['GetSiteContextResponse200OpenRequestsItem']]):
        updated_at (Union[Unset, datetime.datetime]):
    """

    context: "GetSiteContextResponse200Context"
    revision: int
    changed: Union[Unset, bool] = UNSET
    open_requests: Union[Unset, list["GetSiteContextResponse200OpenRequestsItem"]] = UNSET
    updated_at: Union[Unset, datetime.datetime] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        context = self.context.to_dict()

        revision = self.revision

        changed = self.changed

        open_requests: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.open_requests, Unset):
            open_requests = []
            for open_requests_item_data in self.open_requests:
                open_requests_item = open_requests_item_data.to_dict()
                open_requests.append(open_requests_item)

        updated_at: Union[Unset, str] = UNSET
        if not isinstance(self.updated_at, Unset):
            updated_at = self.updated_at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "context": context,
                "revision": revision,
            }
        )
        if changed is not UNSET:
            field_dict["changed"] = changed
        if open_requests is not UNSET:
            field_dict["openRequests"] = open_requests
        if updated_at is not UNSET:
            field_dict["updatedAt"] = updated_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.get_site_context_response_200_context import (
            GetSiteContextResponse200Context,
        )
        from ..models.get_site_context_response_200_open_requests_item import (
            GetSiteContextResponse200OpenRequestsItem,
        )

        d = dict(src_dict)
        context = GetSiteContextResponse200Context.from_dict(d.pop("context"))

        revision = d.pop("revision")

        changed = d.pop("changed", UNSET)

        open_requests = []
        _open_requests = d.pop("openRequests", UNSET)
        for open_requests_item_data in _open_requests or []:
            open_requests_item = GetSiteContextResponse200OpenRequestsItem.from_dict(open_requests_item_data)

            open_requests.append(open_requests_item)

        _updated_at = d.pop("updatedAt", UNSET)
        updated_at: Union[Unset, datetime.datetime]
        if isinstance(_updated_at, Unset):
            updated_at = UNSET
        else:
            updated_at = isoparse(_updated_at)

        get_site_context_response_200 = cls(
            context=context,
            revision=revision,
            changed=changed,
            open_requests=open_requests,
            updated_at=updated_at,
        )

        get_site_context_response_200.additional_properties = d
        return get_site_context_response_200

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
