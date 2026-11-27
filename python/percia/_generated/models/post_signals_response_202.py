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
    from ..models.post_signals_response_202_rejected_item import (
        PostSignalsResponse202RejectedItem,
    )


T = TypeVar("T", bound="PostSignalsResponse202")


@_attrs_define
class PostSignalsResponse202:
    """
    Attributes:
        accepted (int):
        rejected (list['PostSignalsResponse202RejectedItem']):
        stored (Union[Unset, int]): Accepted minus repeats (same channel and seq).
    """

    accepted: int
    rejected: list["PostSignalsResponse202RejectedItem"]
    stored: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        accepted = self.accepted

        rejected = []
        for rejected_item_data in self.rejected:
            rejected_item = rejected_item_data.to_dict()
            rejected.append(rejected_item)

        stored = self.stored

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "accepted": accepted,
                "rejected": rejected,
            }
        )
        if stored is not UNSET:
            field_dict["stored"] = stored

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.post_signals_response_202_rejected_item import (
            PostSignalsResponse202RejectedItem,
        )

        d = dict(src_dict)
        accepted = d.pop("accepted")

        rejected = []
        _rejected = d.pop("rejected")
        for rejected_item_data in _rejected:
            rejected_item = PostSignalsResponse202RejectedItem.from_dict(rejected_item_data)

            rejected.append(rejected_item)

        stored = d.pop("stored", UNSET)

        post_signals_response_202 = cls(
            accepted=accepted,
            rejected=rejected,
            stored=stored,
        )

        post_signals_response_202.additional_properties = d
        return post_signals_response_202

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
