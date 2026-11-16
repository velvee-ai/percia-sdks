from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.update_watch_body_interpretation_concerns_item import (
        UpdateWatchBodyInterpretationConcernsItem,
    )


T = TypeVar("T", bound="UpdateWatchBodyInterpretation")


@_attrs_define
class UpdateWatchBodyInterpretation:
    """
    Attributes:
        concerns (list['UpdateWatchBodyInterpretationConcernsItem']):
    """

    concerns: list["UpdateWatchBodyInterpretationConcernsItem"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        concerns = []
        for concerns_item_data in self.concerns:
            concerns_item = concerns_item_data.to_dict()
            concerns.append(concerns_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "concerns": concerns,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.update_watch_body_interpretation_concerns_item import (
            UpdateWatchBodyInterpretationConcernsItem,
        )

        d = dict(src_dict)
        concerns = []
        _concerns = d.pop("concerns")
        for concerns_item_data in _concerns:
            concerns_item = UpdateWatchBodyInterpretationConcernsItem.from_dict(concerns_item_data)

            concerns.append(concerns_item)

        update_watch_body_interpretation = cls(
            concerns=concerns,
        )

        update_watch_body_interpretation.additional_properties = d
        return update_watch_body_interpretation

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
