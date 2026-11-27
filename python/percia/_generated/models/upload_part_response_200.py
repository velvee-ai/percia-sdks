from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="UploadPartResponse200")


@_attrs_define
class UploadPartResponse200:
    """
    Attributes:
        etag (Union[Unset, str]):
        part_number (Union[Unset, int]):
    """

    etag: Union[Unset, str] = UNSET
    part_number: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        etag = self.etag

        part_number = self.part_number

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if etag is not UNSET:
            field_dict["etag"] = etag
        if part_number is not UNSET:
            field_dict["partNumber"] = part_number

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        etag = d.pop("etag", UNSET)

        part_number = d.pop("partNumber", UNSET)

        upload_part_response_200 = cls(
            etag=etag,
            part_number=part_number,
        )

        upload_part_response_200.additional_properties = d
        return upload_part_response_200

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
