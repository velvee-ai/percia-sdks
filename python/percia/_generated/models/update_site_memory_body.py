from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.update_site_memory_body_entities_item import (
        UpdateSiteMemoryBodyEntitiesItem,
    )


T = TypeVar("T", bound="UpdateSiteMemoryBody")


@_attrs_define
class UpdateSiteMemoryBody:
    """
    Attributes:
        brief (Union[Unset, str]):
        entities (Union[Unset, list['UpdateSiteMemoryBodyEntitiesItem']]):
    """

    brief: Union[Unset, str] = UNSET
    entities: Union[Unset, list["UpdateSiteMemoryBodyEntitiesItem"]] = UNSET

    def to_dict(self) -> dict[str, Any]:
        brief = self.brief

        entities: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.entities, Unset):
            entities = []
            for entities_item_data in self.entities:
                entities_item = entities_item_data.to_dict()
                entities.append(entities_item)

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if brief is not UNSET:
            field_dict["brief"] = brief
        if entities is not UNSET:
            field_dict["entities"] = entities

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.update_site_memory_body_entities_item import (
            UpdateSiteMemoryBodyEntitiesItem,
        )

        d = dict(src_dict)
        brief = d.pop("brief", UNSET)

        entities = []
        _entities = d.pop("entities", UNSET)
        for entities_item_data in _entities or []:
            entities_item = UpdateSiteMemoryBodyEntitiesItem.from_dict(entities_item_data)

            entities.append(entities_item)

        update_site_memory_body = cls(
            brief=brief,
            entities=entities,
        )

        return update_site_memory_body
