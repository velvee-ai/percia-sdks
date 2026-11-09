import datetime
from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
    cast,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="SiteSummary")


@_attrs_define
class SiteSummary:
    """
    Attributes:
        id (Union[Unset, str]):
        memory_updated_at (Union[None, Unset, datetime.datetime]):
        name (Union[Unset, str]):
        watch_count (Union[Unset, int]):
    """

    id: Union[Unset, str] = UNSET
    memory_updated_at: Union[None, Unset, datetime.datetime] = UNSET
    name: Union[Unset, str] = UNSET
    watch_count: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        memory_updated_at: Union[None, Unset, str]
        if isinstance(self.memory_updated_at, Unset):
            memory_updated_at = UNSET
        elif isinstance(self.memory_updated_at, datetime.datetime):
            memory_updated_at = self.memory_updated_at.isoformat()
        else:
            memory_updated_at = self.memory_updated_at

        name = self.name

        watch_count = self.watch_count

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if memory_updated_at is not UNSET:
            field_dict["memoryUpdatedAt"] = memory_updated_at
        if name is not UNSET:
            field_dict["name"] = name
        if watch_count is not UNSET:
            field_dict["watchCount"] = watch_count

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id", UNSET)

        def _parse_memory_updated_at(
            data: object,
        ) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                memory_updated_at_type_0 = isoparse(data)

                return memory_updated_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        memory_updated_at = _parse_memory_updated_at(d.pop("memoryUpdatedAt", UNSET))

        name = d.pop("name", UNSET)

        watch_count = d.pop("watchCount", UNSET)

        site_summary = cls(
            id=id,
            memory_updated_at=memory_updated_at,
            name=name,
            watch_count=watch_count,
        )

        site_summary.additional_properties = d
        return site_summary

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
