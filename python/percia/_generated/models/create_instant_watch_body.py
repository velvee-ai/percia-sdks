from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="CreateInstantWatchBody")


@_attrs_define
class CreateInstantWatchBody:
    """
    Attributes:
        goal (str):
        source_url (str):
        webhook_url (str):
    """

    goal: str
    source_url: str
    webhook_url: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        goal = self.goal

        source_url = self.source_url

        webhook_url = self.webhook_url

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "goal": goal,
                "sourceUrl": source_url,
                "webhookUrl": webhook_url,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        goal = d.pop("goal")

        source_url = d.pop("sourceUrl")

        webhook_url = d.pop("webhookUrl")

        create_instant_watch_body = cls(
            goal=goal,
            source_url=source_url,
            webhook_url=webhook_url,
        )

        create_instant_watch_body.additional_properties = d
        return create_instant_watch_body

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
