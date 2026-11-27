from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.post_signals_response_202_rejected_item_code import (
    PostSignalsResponse202RejectedItemCode,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="PostSignalsResponse202RejectedItem")


@_attrs_define
class PostSignalsResponse202RejectedItem:
    """
    Attributes:
        code (Union[Unset, PostSignalsResponse202RejectedItemCode]):
        field (Union[Unset, str]):
        index (Union[Unset, int]):
        message (Union[Unset, str]):
    """

    code: Union[Unset, PostSignalsResponse202RejectedItemCode] = UNSET
    field: Union[Unset, str] = UNSET
    index: Union[Unset, int] = UNSET
    message: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        code: Union[Unset, str] = UNSET
        if not isinstance(self.code, Unset):
            code = self.code.value

        field = self.field

        index = self.index

        message = self.message

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if code is not UNSET:
            field_dict["code"] = code
        if field is not UNSET:
            field_dict["field"] = field
        if index is not UNSET:
            field_dict["index"] = index
        if message is not UNSET:
            field_dict["message"] = message

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _code = d.pop("code", UNSET)
        code: Union[Unset, PostSignalsResponse202RejectedItemCode]
        if isinstance(_code, Unset):
            code = UNSET
        else:
            code = PostSignalsResponse202RejectedItemCode(_code)

        field = d.pop("field", UNSET)

        index = d.pop("index", UNSET)

        message = d.pop("message", UNSET)

        post_signals_response_202_rejected_item = cls(
            code=code,
            field=field,
            index=index,
            message=message,
        )

        post_signals_response_202_rejected_item.additional_properties = d
        return post_signals_response_202_rejected_item

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
