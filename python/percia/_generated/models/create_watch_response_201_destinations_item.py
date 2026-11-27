from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateWatchResponse201DestinationsItem")


@_attrs_define
class CreateWatchResponse201DestinationsItem:
    """
    Attributes:
        connection_id (Union[Unset, str]):
        label (Union[Unset, str]):
        service (Union[Unset, str]):
    """

    connection_id: Union[Unset, str] = UNSET
    label: Union[Unset, str] = UNSET
    service: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        connection_id = self.connection_id

        label = self.label

        service = self.service

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if connection_id is not UNSET:
            field_dict["connectionId"] = connection_id
        if label is not UNSET:
            field_dict["label"] = label
        if service is not UNSET:
            field_dict["service"] = service

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        connection_id = d.pop("connectionId", UNSET)

        label = d.pop("label", UNSET)

        service = d.pop("service", UNSET)

        create_watch_response_201_destinations_item = cls(
            connection_id=connection_id,
            label=label,
            service=service,
        )

        create_watch_response_201_destinations_item.additional_properties = d
        return create_watch_response_201_destinations_item

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
