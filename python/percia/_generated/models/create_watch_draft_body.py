from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateWatchDraftBody")


@_attrs_define
class CreateWatchDraftBody:
    """
    Attributes:
        goal (str):
        camera_id (Union[Unset, str]):
        source_url (Union[Unset, str]):
    """

    goal: str
    camera_id: Union[Unset, str] = UNSET
    source_url: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        goal = self.goal

        camera_id = self.camera_id

        source_url = self.source_url

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "goal": goal,
            }
        )
        if camera_id is not UNSET:
            field_dict["cameraId"] = camera_id
        if source_url is not UNSET:
            field_dict["sourceUrl"] = source_url

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        goal = d.pop("goal")

        camera_id = d.pop("cameraId", UNSET)

        source_url = d.pop("sourceUrl", UNSET)

        create_watch_draft_body = cls(
            goal=goal,
            camera_id=camera_id,
            source_url=source_url,
        )

        create_watch_draft_body.additional_properties = d
        return create_watch_draft_body

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
