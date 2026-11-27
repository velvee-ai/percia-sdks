from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
    Union,
    cast,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.report_miss_response_201_engine import ReportMissResponse201Engine


T = TypeVar("T", bound="ReportMissResponse201")


@_attrs_define
class ReportMissResponse201:
    """
    Attributes:
        concern_id (Union[None, Unset, str]):
        engine (Union[Unset, ReportMissResponse201Engine]):
        from_ (Union[Unset, str]):
        id (Union[Unset, str]):
        to (Union[Unset, str]):
        watch_id (Union[Unset, str]):
    """

    concern_id: Union[None, Unset, str] = UNSET
    engine: Union[Unset, "ReportMissResponse201Engine"] = UNSET
    from_: Union[Unset, str] = UNSET
    id: Union[Unset, str] = UNSET
    to: Union[Unset, str] = UNSET
    watch_id: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        concern_id: Union[None, Unset, str]
        if isinstance(self.concern_id, Unset):
            concern_id = UNSET
        else:
            concern_id = self.concern_id

        engine: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.engine, Unset):
            engine = self.engine.to_dict()

        from_ = self.from_

        id = self.id

        to = self.to

        watch_id = self.watch_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if concern_id is not UNSET:
            field_dict["concernId"] = concern_id
        if engine is not UNSET:
            field_dict["engine"] = engine
        if from_ is not UNSET:
            field_dict["from"] = from_
        if id is not UNSET:
            field_dict["id"] = id
        if to is not UNSET:
            field_dict["to"] = to
        if watch_id is not UNSET:
            field_dict["watchId"] = watch_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.report_miss_response_201_engine import ReportMissResponse201Engine

        d = dict(src_dict)

        def _parse_concern_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        concern_id = _parse_concern_id(d.pop("concernId", UNSET))

        _engine = d.pop("engine", UNSET)
        engine: Union[Unset, ReportMissResponse201Engine]
        if isinstance(_engine, Unset):
            engine = UNSET
        else:
            engine = ReportMissResponse201Engine.from_dict(_engine)

        from_ = d.pop("from", UNSET)

        id = d.pop("id", UNSET)

        to = d.pop("to", UNSET)

        watch_id = d.pop("watchId", UNSET)

        report_miss_response_201 = cls(
            concern_id=concern_id,
            engine=engine,
            from_=from_,
            id=id,
            to=to,
            watch_id=watch_id,
        )

        report_miss_response_201.additional_properties = d
        return report_miss_response_201

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
