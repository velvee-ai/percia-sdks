from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="UpdateIntegrationBody")


@_attrs_define
class UpdateIntegrationBody:
    """
    Attributes:
        default (bool): Attach this destination to every new watch.
        apply_to_existing (Union[Unset, bool]): With default: true, also add it (on "*") to every watch you own that
            lacks it and has room.
    """

    default: bool
    apply_to_existing: Union[Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        default = self.default

        apply_to_existing = self.apply_to_existing

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "default": default,
            }
        )
        if apply_to_existing is not UNSET:
            field_dict["applyToExisting"] = apply_to_existing

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        default = d.pop("default")

        apply_to_existing = d.pop("applyToExisting", UNSET)

        update_integration_body = cls(
            default=default,
            apply_to_existing=apply_to_existing,
        )

        update_integration_body.additional_properties = d
        return update_integration_body

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
