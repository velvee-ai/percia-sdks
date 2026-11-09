from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.list_integration_services_response_200_item_connect_kind import (
    ListIntegrationServicesResponse200ItemConnectKind,
)
from ..models.list_integration_services_response_200_item_service import (
    ListIntegrationServicesResponse200ItemService,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="ListIntegrationServicesResponse200Item")


@_attrs_define
class ListIntegrationServicesResponse200Item:
    """
    Attributes:
        available (Union[Unset, bool]):
        connect_kind (Union[Unset, ListIntegrationServicesResponse200ItemConnectKind]): oauth: the service's own
            approval page. deeplink: a link that opens the bot. url: the person pastes a URL. key: a key and an event name.
            fields: account details (SMS, WhatsApp).
        name (Union[Unset, str]):
        service (Union[Unset, ListIntegrationServicesResponse200ItemService]):
    """

    available: Union[Unset, bool] = UNSET
    connect_kind: Union[Unset, ListIntegrationServicesResponse200ItemConnectKind] = UNSET
    name: Union[Unset, str] = UNSET
    service: Union[Unset, ListIntegrationServicesResponse200ItemService] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        available = self.available

        connect_kind: Union[Unset, str] = UNSET
        if not isinstance(self.connect_kind, Unset):
            connect_kind = self.connect_kind.value

        name = self.name

        service: Union[Unset, str] = UNSET
        if not isinstance(self.service, Unset):
            service = self.service.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if available is not UNSET:
            field_dict["available"] = available
        if connect_kind is not UNSET:
            field_dict["connectKind"] = connect_kind
        if name is not UNSET:
            field_dict["name"] = name
        if service is not UNSET:
            field_dict["service"] = service

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        available = d.pop("available", UNSET)

        _connect_kind = d.pop("connectKind", UNSET)
        connect_kind: Union[Unset, ListIntegrationServicesResponse200ItemConnectKind]
        if isinstance(_connect_kind, Unset):
            connect_kind = UNSET
        else:
            connect_kind = ListIntegrationServicesResponse200ItemConnectKind(_connect_kind)

        name = d.pop("name", UNSET)

        _service = d.pop("service", UNSET)
        service: Union[Unset, ListIntegrationServicesResponse200ItemService]
        if isinstance(_service, Unset):
            service = UNSET
        else:
            service = ListIntegrationServicesResponse200ItemService(_service)

        list_integration_services_response_200_item = cls(
            available=available,
            connect_kind=connect_kind,
            name=name,
            service=service,
        )

        list_integration_services_response_200_item.additional_properties = d
        return list_integration_services_response_200_item

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
