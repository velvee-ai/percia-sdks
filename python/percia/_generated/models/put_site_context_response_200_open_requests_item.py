from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.put_site_context_response_200_open_requests_item_request import (
        PutSiteContextResponse200OpenRequestsItemRequest,
    )


T = TypeVar("T", bound="PutSiteContextResponse200OpenRequestsItem")


@_attrs_define
class PutSiteContextResponse200OpenRequestsItem:
    """
    Attributes:
        request (Union[Unset, PutSiteContextResponse200OpenRequestsItemRequest]): A context request: item, name, why,
            how_to_supply, required, degraded_mode.
        watch_id (Union[Unset, str]):
    """

    request: Union[Unset, "PutSiteContextResponse200OpenRequestsItemRequest"] = UNSET
    watch_id: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        request: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.request, Unset):
            request = self.request.to_dict()

        watch_id = self.watch_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if request is not UNSET:
            field_dict["request"] = request
        if watch_id is not UNSET:
            field_dict["watchId"] = watch_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.put_site_context_response_200_open_requests_item_request import (
            PutSiteContextResponse200OpenRequestsItemRequest,
        )

        d = dict(src_dict)
        _request = d.pop("request", UNSET)
        request: Union[Unset, PutSiteContextResponse200OpenRequestsItemRequest]
        if isinstance(_request, Unset):
            request = UNSET
        else:
            request = PutSiteContextResponse200OpenRequestsItemRequest.from_dict(_request)

        watch_id = d.pop("watchId", UNSET)

        put_site_context_response_200_open_requests_item = cls(
            request=request,
            watch_id=watch_id,
        )

        put_site_context_response_200_open_requests_item.additional_properties = d
        return put_site_context_response_200_open_requests_item

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
