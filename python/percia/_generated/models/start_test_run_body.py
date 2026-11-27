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

from ..models.start_test_run_body_source import StartTestRunBodySource
from ..types import UNSET, Unset

T = TypeVar("T", bound="StartTestRunBody")


@_attrs_define
class StartTestRunBody:
    """
    Attributes:
        source (StartTestRunBodySource):
        from_ (Union[Unset, datetime.datetime]):
        minutes (Union[Unset, float]):
    """

    source: StartTestRunBodySource
    from_: Union[Unset, datetime.datetime] = UNSET
    minutes: Union[Unset, float] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        source = self.source.value

        from_: Union[Unset, str] = UNSET
        if not isinstance(self.from_, Unset):
            from_ = self.from_.isoformat()

        minutes = self.minutes

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "source": source,
            }
        )
        if from_ is not UNSET:
            field_dict["from"] = from_
        if minutes is not UNSET:
            field_dict["minutes"] = minutes

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        source = StartTestRunBodySource(d.pop("source"))

        _from_ = d.pop("from", UNSET)
        from_: Union[Unset, datetime.datetime]
        if isinstance(_from_, Unset):
            from_ = UNSET
        else:
            from_ = isoparse(_from_)

        minutes = d.pop("minutes", UNSET)

        start_test_run_body = cls(
            source=source,
            from_=from_,
            minutes=minutes,
        )

        start_test_run_body.additional_properties = d
        return start_test_run_body

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
