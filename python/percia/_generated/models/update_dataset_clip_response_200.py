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
    from ..models.update_dataset_clip_response_200_clip import (
        UpdateDatasetClipResponse200Clip,
    )


T = TypeVar("T", bound="UpdateDatasetClipResponse200")


@_attrs_define
class UpdateDatasetClipResponse200:
    """
    Attributes:
        clip (Union[Unset, UpdateDatasetClipResponse200Clip]):
    """

    clip: Union[Unset, "UpdateDatasetClipResponse200Clip"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        clip: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.clip, Unset):
            clip = self.clip.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if clip is not UNSET:
            field_dict["clip"] = clip

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.update_dataset_clip_response_200_clip import (
            UpdateDatasetClipResponse200Clip,
        )

        d = dict(src_dict)
        _clip = d.pop("clip", UNSET)
        clip: Union[Unset, UpdateDatasetClipResponse200Clip]
        if isinstance(_clip, Unset):
            clip = UNSET
        else:
            clip = UpdateDatasetClipResponse200Clip.from_dict(_clip)

        update_dataset_clip_response_200 = cls(
            clip=clip,
        )

        update_dataset_clip_response_200.additional_properties = d
        return update_dataset_clip_response_200

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
