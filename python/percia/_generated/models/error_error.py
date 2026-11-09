from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.error_error_code import ErrorErrorCode
from ..types import UNSET, Unset

T = TypeVar("T", bound="ErrorError")


@_attrs_define
class ErrorError:
    """
    Attributes:
        code (ErrorErrorCode):
        message (str):
        field (Union[Unset, str]): Name of the offending request field, on validation errors.
        request_id (Union[Unset, str]): The id of this request, also in the x-percia-request-id header. Quote it when
            reporting a problem.
    """

    code: ErrorErrorCode
    message: str
    field: Union[Unset, str] = UNSET
    request_id: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        code = self.code.value

        message = self.message

        field = self.field

        request_id = self.request_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "code": code,
                "message": message,
            }
        )
        if field is not UNSET:
            field_dict["field"] = field
        if request_id is not UNSET:
            field_dict["request_id"] = request_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        code = ErrorErrorCode(d.pop("code"))

        message = d.pop("message")

        field = d.pop("field", UNSET)

        request_id = d.pop("request_id", UNSET)

        error_error = cls(
            code=code,
            message=message,
            field=field,
            request_id=request_id,
        )

        error_error.additional_properties = d
        return error_error

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
