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
    from ..models.list_dataset_clips_response_200_clips_item import (
        ListDatasetClipsResponse200ClipsItem,
    )
    from ..models.list_dataset_clips_response_200_counts import (
        ListDatasetClipsResponse200Counts,
    )


T = TypeVar("T", bound="ListDatasetClipsResponse200")


@_attrs_define
class ListDatasetClipsResponse200:
    """
    Attributes:
        clips (Union[Unset, list['ListDatasetClipsResponse200ClipsItem']]):
        counts (Union[Unset, ListDatasetClipsResponse200Counts]):
        total (Union[Unset, int]):
    """

    clips: Union[Unset, list["ListDatasetClipsResponse200ClipsItem"]] = UNSET
    counts: Union[Unset, "ListDatasetClipsResponse200Counts"] = UNSET
    total: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        clips: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.clips, Unset):
            clips = []
            for clips_item_data in self.clips:
                clips_item = clips_item_data.to_dict()
                clips.append(clips_item)

        counts: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.counts, Unset):
            counts = self.counts.to_dict()

        total = self.total

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if clips is not UNSET:
            field_dict["clips"] = clips
        if counts is not UNSET:
            field_dict["counts"] = counts
        if total is not UNSET:
            field_dict["total"] = total

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.list_dataset_clips_response_200_clips_item import (
            ListDatasetClipsResponse200ClipsItem,
        )
        from ..models.list_dataset_clips_response_200_counts import (
            ListDatasetClipsResponse200Counts,
        )

        d = dict(src_dict)
        clips = []
        _clips = d.pop("clips", UNSET)
        for clips_item_data in _clips or []:
            clips_item = ListDatasetClipsResponse200ClipsItem.from_dict(clips_item_data)

            clips.append(clips_item)

        _counts = d.pop("counts", UNSET)
        counts: Union[Unset, ListDatasetClipsResponse200Counts]
        if isinstance(_counts, Unset):
            counts = UNSET
        else:
            counts = ListDatasetClipsResponse200Counts.from_dict(_counts)

        total = d.pop("total", UNSET)

        list_dataset_clips_response_200 = cls(
            clips=clips,
            counts=counts,
            total=total,
        )

        list_dataset_clips_response_200.additional_properties = d
        return list_dataset_clips_response_200

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
