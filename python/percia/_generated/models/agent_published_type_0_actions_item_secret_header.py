from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="AgentPublishedType0ActionsItemSecretHeader")


@_attrs_define
class AgentPublishedType0ActionsItemSecretHeader:
    """
    Attributes:
        name (str):
        has_secret (Union[Unset, bool]): Read only.
        value (Union[Unset, str]): Write only.
    """

    name: str
    has_secret: Union[Unset, bool] = UNSET
    value: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        has_secret = self.has_secret

        value = self.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
            }
        )
        if has_secret is not UNSET:
            field_dict["hasSecret"] = has_secret
        if value is not UNSET:
            field_dict["value"] = value

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        has_secret = d.pop("hasSecret", UNSET)

        value = d.pop("value", UNSET)

        agent_published_type_0_actions_item_secret_header = cls(
            name=name,
            has_secret=has_secret,
            value=value,
        )

        agent_published_type_0_actions_item_secret_header.additional_properties = d
        return agent_published_type_0_actions_item_secret_header

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
