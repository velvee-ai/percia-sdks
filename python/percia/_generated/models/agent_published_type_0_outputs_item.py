from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
    cast,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.agent_published_type_0_outputs_item_type import (
    AgentPublishedType0OutputsItemType,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="AgentPublishedType0OutputsItem")


@_attrs_define
class AgentPublishedType0OutputsItem:
    """
    Attributes:
        description (str):
        name (str): Identifier, at most 32 characters.
        type_ (AgentPublishedType0OutputsItemType):
        options (Union[Unset, list[str]]): Required for enum, 2 to 20 values.
    """

    description: str
    name: str
    type_: AgentPublishedType0OutputsItemType
    options: Union[Unset, list[str]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        description = self.description

        name = self.name

        type_ = self.type_.value

        options: Union[Unset, list[str]] = UNSET
        if not isinstance(self.options, Unset):
            options = self.options

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "description": description,
                "name": name,
                "type": type_,
            }
        )
        if options is not UNSET:
            field_dict["options"] = options

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        description = d.pop("description")

        name = d.pop("name")

        type_ = AgentPublishedType0OutputsItemType(d.pop("type"))

        options = cast(list[str], d.pop("options", UNSET))

        agent_published_type_0_outputs_item = cls(
            description=description,
            name=name,
            type_=type_,
            options=options,
        )

        agent_published_type_0_outputs_item.additional_properties = d
        return agent_published_type_0_outputs_item

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
