from collections.abc import Mapping
from typing import (
    Any,
    Literal,
    TypeVar,
    Union,
    cast,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="UpdateSiteBody")


@_attrs_define
class UpdateSiteBody:
    """
    Attributes:
        name (Union[Unset, str]):
        notes (Union[Unset, str]):
        retention_days (Union[Literal[14], Literal[1], Literal[30], Literal[3], Literal[7], None, Unset]):
    """

    name: Union[Unset, str] = UNSET
    notes: Union[Unset, str] = UNSET
    retention_days: Union[Literal[14], Literal[1], Literal[30], Literal[3], Literal[7], None, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        notes = self.notes

        retention_days: Union[Literal[14], Literal[1], Literal[30], Literal[3], Literal[7], None, Unset]
        if isinstance(self.retention_days, Unset):
            retention_days = UNSET
        else:
            retention_days = self.retention_days

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if notes is not UNSET:
            field_dict["notes"] = notes
        if retention_days is not UNSET:
            field_dict["retentionDays"] = retention_days

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name", UNSET)

        notes = d.pop("notes", UNSET)

        def _parse_retention_days(
            data: object,
        ) -> Union[Literal[14], Literal[1], Literal[30], Literal[3], Literal[7], None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            retention_days_type_0_type_0 = cast(Literal[1], data)
            if retention_days_type_0_type_0 != 1:
                raise ValueError(
                    f"retentionDays_type_0_type_0 must match const 1, got '{retention_days_type_0_type_0}'"
                )
            return retention_days_type_0_type_0
            retention_days_type_0_type_1 = cast(Literal[3], data)
            if retention_days_type_0_type_1 != 3:
                raise ValueError(
                    f"retentionDays_type_0_type_1 must match const 3, got '{retention_days_type_0_type_1}'"
                )
            return retention_days_type_0_type_1
            retention_days_type_0_type_2 = cast(Literal[7], data)
            if retention_days_type_0_type_2 != 7:
                raise ValueError(
                    f"retentionDays_type_0_type_2 must match const 7, got '{retention_days_type_0_type_2}'"
                )
            return retention_days_type_0_type_2
            retention_days_type_0_type_3 = cast(Literal[14], data)
            if retention_days_type_0_type_3 != 14:
                raise ValueError(
                    f"retentionDays_type_0_type_3 must match const 14, got '{retention_days_type_0_type_3}'"
                )
            return retention_days_type_0_type_3
            retention_days_type_0_type_4 = cast(Literal[30], data)
            if retention_days_type_0_type_4 != 30:
                raise ValueError(
                    f"retentionDays_type_0_type_4 must match const 30, got '{retention_days_type_0_type_4}'"
                )
            return retention_days_type_0_type_4
            return cast(
                Union[
                    Literal[14],
                    Literal[1],
                    Literal[30],
                    Literal[3],
                    Literal[7],
                    None,
                    Unset,
                ],
                data,
            )

        retention_days = _parse_retention_days(d.pop("retentionDays", UNSET))

        update_site_body = cls(
            name=name,
            notes=notes,
            retention_days=retention_days,
        )

        update_site_body.additional_properties = d
        return update_site_body

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
