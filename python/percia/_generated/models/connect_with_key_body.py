from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.connect_with_key_body_severity import ConnectWithKeyBodySeverity
from ..types import UNSET, Unset

T = TypeVar("T", bound="ConnectWithKeyBody")


@_attrs_define
class ConnectWithKeyBody:
    """
    Attributes:
        key (str):
        default (Union[Unset, bool]):
        event (Union[Unset, str]):
        label (Union[Unset, str]):
        severity (Union[Unset, ConnectWithKeyBodySeverity]):
    """

    key: str
    default: Union[Unset, bool] = UNSET
    event: Union[Unset, str] = UNSET
    label: Union[Unset, str] = UNSET
    severity: Union[Unset, ConnectWithKeyBodySeverity] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        key = self.key

        default = self.default

        event = self.event

        label = self.label

        severity: Union[Unset, str] = UNSET
        if not isinstance(self.severity, Unset):
            severity = self.severity.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "key": key,
            }
        )
        if default is not UNSET:
            field_dict["default"] = default
        if event is not UNSET:
            field_dict["event"] = event
        if label is not UNSET:
            field_dict["label"] = label
        if severity is not UNSET:
            field_dict["severity"] = severity

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        key = d.pop("key")

        default = d.pop("default", UNSET)

        event = d.pop("event", UNSET)

        label = d.pop("label", UNSET)

        _severity = d.pop("severity", UNSET)
        severity: Union[Unset, ConnectWithKeyBodySeverity]
        if isinstance(_severity, Unset):
            severity = UNSET
        else:
            severity = ConnectWithKeyBodySeverity(_severity)

        connect_with_key_body = cls(
            key=key,
            default=default,
            event=event,
            label=label,
            severity=severity,
        )

        connect_with_key_body.additional_properties = d
        return connect_with_key_body

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
