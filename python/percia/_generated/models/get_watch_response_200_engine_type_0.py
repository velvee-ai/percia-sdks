from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="GetWatchResponse200EngineType0")


@_attrs_define
class GetWatchResponse200EngineType0:
    """The engine release (Percept version plus Percia's runner revision) that judges this watch, or would when it is
    active. pinned is true when support fixed it for this watch; otherwise it follows Percia's staged rollout. Null
    while none is assigned. Informational: there is nothing to set.

        Attributes:
            id (Union[Unset, str]): Release id, e.g. pv1.1.0-r18.
            percept_version (Union[Unset, str]):
            pinned (Union[Unset, bool]):
    """

    id: Union[Unset, str] = UNSET
    percept_version: Union[Unset, str] = UNSET
    pinned: Union[Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        percept_version = self.percept_version

        pinned = self.pinned

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if percept_version is not UNSET:
            field_dict["perceptVersion"] = percept_version
        if pinned is not UNSET:
            field_dict["pinned"] = pinned

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id", UNSET)

        percept_version = d.pop("perceptVersion", UNSET)

        pinned = d.pop("pinned", UNSET)

        get_watch_response_200_engine_type_0 = cls(
            id=id,
            percept_version=percept_version,
            pinned=pinned,
        )

        get_watch_response_200_engine_type_0.additional_properties = d
        return get_watch_response_200_engine_type_0

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
