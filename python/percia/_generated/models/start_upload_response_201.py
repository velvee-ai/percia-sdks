from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="StartUploadResponse201")


@_attrs_define
class StartUploadResponse201:
    """
    Attributes:
        id (Union[Unset, str]):
        max_seconds (Union[Unset, int]):
        part_size (Union[Unset, int]):
        parts (Union[Unset, int]):
    """

    id: Union[Unset, str] = UNSET
    max_seconds: Union[Unset, int] = UNSET
    part_size: Union[Unset, int] = UNSET
    parts: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        max_seconds = self.max_seconds

        part_size = self.part_size

        parts = self.parts

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if max_seconds is not UNSET:
            field_dict["maxSeconds"] = max_seconds
        if part_size is not UNSET:
            field_dict["partSize"] = part_size
        if parts is not UNSET:
            field_dict["parts"] = parts

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id", UNSET)

        max_seconds = d.pop("maxSeconds", UNSET)

        part_size = d.pop("partSize", UNSET)

        parts = d.pop("parts", UNSET)

        start_upload_response_201 = cls(
            id=id,
            max_seconds=max_seconds,
            part_size=part_size,
            parts=parts,
        )

        start_upload_response_201.additional_properties = d
        return start_upload_response_201

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
