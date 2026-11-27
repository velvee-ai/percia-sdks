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
    from ..models.list_watch_misses_response_200_misses_item import (
        ListWatchMissesResponse200MissesItem,
    )


T = TypeVar("T", bound="ListWatchMissesResponse200")


@_attrs_define
class ListWatchMissesResponse200:
    """
    Attributes:
        misses (Union[Unset, list['ListWatchMissesResponse200MissesItem']]):
    """

    misses: Union[Unset, list["ListWatchMissesResponse200MissesItem"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        misses: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.misses, Unset):
            misses = []
            for misses_item_data in self.misses:
                misses_item = misses_item_data.to_dict()
                misses.append(misses_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if misses is not UNSET:
            field_dict["misses"] = misses

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.list_watch_misses_response_200_misses_item import (
            ListWatchMissesResponse200MissesItem,
        )

        d = dict(src_dict)
        misses = []
        _misses = d.pop("misses", UNSET)
        for misses_item_data in _misses or []:
            misses_item = ListWatchMissesResponse200MissesItem.from_dict(misses_item_data)

            misses.append(misses_item)

        list_watch_misses_response_200 = cls(
            misses=misses,
        )

        list_watch_misses_response_200.additional_properties = d
        return list_watch_misses_response_200

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
