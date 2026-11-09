from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
    cast,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="TestHookResponse200")


@_attrs_define
class TestHookResponse200:
    """
    Attributes:
        error (Union[Unset, str]):
        ms (Union[Unset, int]):
        status (Union[None, Unset, int]):
    """

    error: Union[Unset, str] = UNSET
    ms: Union[Unset, int] = UNSET
    status: Union[None, Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        error = self.error

        ms = self.ms

        status: Union[None, Unset, int]
        if isinstance(self.status, Unset):
            status = UNSET
        else:
            status = self.status

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if error is not UNSET:
            field_dict["error"] = error
        if ms is not UNSET:
            field_dict["ms"] = ms
        if status is not UNSET:
            field_dict["status"] = status

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        error = d.pop("error", UNSET)

        ms = d.pop("ms", UNSET)

        def _parse_status(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        status = _parse_status(d.pop("status", UNSET))

        test_hook_response_200 = cls(
            error=error,
            ms=ms,
            status=status,
        )

        test_hook_response_200.additional_properties = d
        return test_hook_response_200

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
