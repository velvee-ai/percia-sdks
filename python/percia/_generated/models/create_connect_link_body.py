from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.create_connect_link_body_service import CreateConnectLinkBodyService
from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateConnectLinkBody")


@_attrs_define
class CreateConnectLinkBody:
    """
    Attributes:
        service (CreateConnectLinkBodyService):
        default (Union[Unset, bool]): Make the new connection a default destination: attached to every new watch (B40).
    """

    service: CreateConnectLinkBodyService
    default: Union[Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        service = self.service.value

        default = self.default

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "service": service,
            }
        )
        if default is not UNSET:
            field_dict["default"] = default

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        service = CreateConnectLinkBodyService(d.pop("service"))

        default = d.pop("default", UNSET)

        create_connect_link_body = cls(
            service=service,
            default=default,
        )

        create_connect_link_body.additional_properties = d
        return create_connect_link_body

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
