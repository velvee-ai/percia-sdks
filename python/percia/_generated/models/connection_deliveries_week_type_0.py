from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ConnectionDeliveriesWeekType0")


@_attrs_define
class ConnectionDeliveriesWeekType0:
    """Deliveries that reached a final status in the last 7 days. A test send is not counted.

    Attributes:
        delivered (Union[Unset, int]):
        failed (Union[Unset, int]):
    """

    delivered: Union[Unset, int] = UNSET
    failed: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        delivered = self.delivered

        failed = self.failed

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if delivered is not UNSET:
            field_dict["delivered"] = delivered
        if failed is not UNSET:
            field_dict["failed"] = failed

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        delivered = d.pop("delivered", UNSET)

        failed = d.pop("failed", UNSET)

        connection_deliveries_week_type_0 = cls(
            delivered=delivered,
            failed=failed,
        )

        connection_deliveries_week_type_0.additional_properties = d
        return connection_deliveries_week_type_0

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
