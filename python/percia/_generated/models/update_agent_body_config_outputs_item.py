from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
    cast,
)

from attrs import define as _attrs_define

from ..models.update_agent_body_config_outputs_item_type import (
    UpdateAgentBodyConfigOutputsItemType,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="UpdateAgentBodyConfigOutputsItem")


@_attrs_define
class UpdateAgentBodyConfigOutputsItem:
    """
    Attributes:
        description (str):
        name (str):
        type_ (UpdateAgentBodyConfigOutputsItemType):
        options (Union[Unset, list[str]]):
    """

    description: str
    name: str
    type_: UpdateAgentBodyConfigOutputsItemType
    options: Union[Unset, list[str]] = UNSET

    def to_dict(self) -> dict[str, Any]:
        description = self.description

        name = self.name

        type_ = self.type_.value

        options: Union[Unset, list[str]] = UNSET
        if not isinstance(self.options, Unset):
            options = self.options

        field_dict: dict[str, Any] = {}

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

        type_ = UpdateAgentBodyConfigOutputsItemType(d.pop("type"))

        options = cast(list[str], d.pop("options", UNSET))

        update_agent_body_config_outputs_item = cls(
            description=description,
            name=name,
            type_=type_,
            options=options,
        )

        return update_agent_body_config_outputs_item
