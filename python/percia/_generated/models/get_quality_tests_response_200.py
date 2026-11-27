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
    from ..models.get_quality_tests_response_200_clips import (
        GetQualityTestsResponse200Clips,
    )
    from ..models.get_quality_tests_response_200_watches import (
        GetQualityTestsResponse200Watches,
    )


T = TypeVar("T", bound="GetQualityTestsResponse200")


@_attrs_define
class GetQualityTestsResponse200:
    """
    Attributes:
        clips (Union[Unset, GetQualityTestsResponse200Clips]):
        tests_week (Union[Unset, int]):
        watches (Union[Unset, GetQualityTestsResponse200Watches]):
    """

    clips: Union[Unset, "GetQualityTestsResponse200Clips"] = UNSET
    tests_week: Union[Unset, int] = UNSET
    watches: Union[Unset, "GetQualityTestsResponse200Watches"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        clips: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.clips, Unset):
            clips = self.clips.to_dict()

        tests_week = self.tests_week

        watches: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.watches, Unset):
            watches = self.watches.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if clips is not UNSET:
            field_dict["clips"] = clips
        if tests_week is not UNSET:
            field_dict["testsWeek"] = tests_week
        if watches is not UNSET:
            field_dict["watches"] = watches

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.get_quality_tests_response_200_clips import (
            GetQualityTestsResponse200Clips,
        )
        from ..models.get_quality_tests_response_200_watches import (
            GetQualityTestsResponse200Watches,
        )

        d = dict(src_dict)
        _clips = d.pop("clips", UNSET)
        clips: Union[Unset, GetQualityTestsResponse200Clips]
        if isinstance(_clips, Unset):
            clips = UNSET
        else:
            clips = GetQualityTestsResponse200Clips.from_dict(_clips)

        tests_week = d.pop("testsWeek", UNSET)

        _watches = d.pop("watches", UNSET)
        watches: Union[Unset, GetQualityTestsResponse200Watches]
        if isinstance(_watches, Unset):
            watches = UNSET
        else:
            watches = GetQualityTestsResponse200Watches.from_dict(_watches)

        get_quality_tests_response_200 = cls(
            clips=clips,
            tests_week=tests_week,
            watches=watches,
        )

        get_quality_tests_response_200.additional_properties = d
        return get_quality_tests_response_200

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
