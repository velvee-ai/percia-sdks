from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.error_error import ErrorError


T = TypeVar("T", bound="Error")


@_attrs_define
class Error:
    """Every API error. `error.code` is stable; `message` is repeated at the top level for older clients. 429 responses
    carry a Retry-After header (seconds).

        Attributes:
            error (ErrorError):
            message (str):
            request_id (Union[Unset, str]): Same as error.request_id.
    """

    error: "ErrorError"
    message: str
    request_id: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        error = self.error.to_dict()

        message = self.message

        request_id = self.request_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "error": error,
                "message": message,
            }
        )
        if request_id is not UNSET:
            field_dict["request_id"] = request_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.error_error import ErrorError

        d = dict(src_dict)
        error = ErrorError.from_dict(d.pop("error"))

        message = d.pop("message")

        request_id = d.pop("request_id", UNSET)

        error = cls(
            error=error,
            message=message,
            request_id=request_id,
        )

        error.additional_properties = d
        return error

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
