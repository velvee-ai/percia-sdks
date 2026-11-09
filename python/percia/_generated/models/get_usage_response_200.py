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
    from ..models.get_usage_response_200_rows_item import GetUsageResponse200RowsItem
    from ..models.get_usage_response_200_totals import GetUsageResponse200Totals


T = TypeVar("T", bound="GetUsageResponse200")


@_attrs_define
class GetUsageResponse200:
    """
    Attributes:
        days (Union[Unset, int]):
        rows (Union[Unset, list['GetUsageResponse200RowsItem']]):
        totals (Union[Unset, GetUsageResponse200Totals]):
    """

    days: Union[Unset, int] = UNSET
    rows: Union[Unset, list["GetUsageResponse200RowsItem"]] = UNSET
    totals: Union[Unset, "GetUsageResponse200Totals"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        days = self.days

        rows: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.rows, Unset):
            rows = []
            for rows_item_data in self.rows:
                rows_item = rows_item_data.to_dict()
                rows.append(rows_item)

        totals: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.totals, Unset):
            totals = self.totals.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if days is not UNSET:
            field_dict["days"] = days
        if rows is not UNSET:
            field_dict["rows"] = rows
        if totals is not UNSET:
            field_dict["totals"] = totals

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.get_usage_response_200_rows_item import (
            GetUsageResponse200RowsItem,
        )
        from ..models.get_usage_response_200_totals import GetUsageResponse200Totals

        d = dict(src_dict)
        days = d.pop("days", UNSET)

        rows = []
        _rows = d.pop("rows", UNSET)
        for rows_item_data in _rows or []:
            rows_item = GetUsageResponse200RowsItem.from_dict(rows_item_data)

            rows.append(rows_item)

        _totals = d.pop("totals", UNSET)
        totals: Union[Unset, GetUsageResponse200Totals]
        if isinstance(_totals, Unset):
            totals = UNSET
        else:
            totals = GetUsageResponse200Totals.from_dict(_totals)

        get_usage_response_200 = cls(
            days=days,
            rows=rows,
            totals=totals,
        )

        get_usage_response_200.additional_properties = d
        return get_usage_response_200

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
