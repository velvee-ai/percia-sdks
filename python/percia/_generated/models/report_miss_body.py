import datetime
from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="ReportMissBody")


@_attrs_define
class ReportMissBody:
    """
    Attributes:
        from_ (datetime.datetime):
        to (datetime.datetime):
        concern_id (Union[Unset, str]):
        note (Union[Unset, str]):
    """

    from_: datetime.datetime
    to: datetime.datetime
    concern_id: Union[Unset, str] = UNSET
    note: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from_ = self.from_.isoformat()

        to = self.to.isoformat()

        concern_id = self.concern_id

        note = self.note

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "from": from_,
                "to": to,
            }
        )
        if concern_id is not UNSET:
            field_dict["concernId"] = concern_id
        if note is not UNSET:
            field_dict["note"] = note

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        from_ = isoparse(d.pop("from"))

        to = isoparse(d.pop("to"))

        concern_id = d.pop("concernId", UNSET)

        note = d.pop("note", UNSET)

        report_miss_body = cls(
            from_=from_,
            to=to,
            concern_id=concern_id,
            note=note,
        )

        report_miss_body.additional_properties = d
        return report_miss_body

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
