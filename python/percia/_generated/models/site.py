import datetime
from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
    Union,
    cast,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.site_region import SiteRegion
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.entity import Entity
    from ..models.site_watches_item import SiteWatchesItem


T = TypeVar("T", bound="Site")


@_attrs_define
class Site:
    """
    Attributes:
        brief (Union[Unset, str]): Model-written, at most 1500 characters. Untrusted.
        entities (Union[Unset, list['Entity']]):
        id (Union[Unset, str]):
        memory_error (Union[None, Unset, str]): model_unavailable or invalid_output after the last failed update; the
            previous memory is kept.
        memory_rev (Union[Unset, int]):
        memory_updated_at (Union[None, Unset, datetime.datetime]):
        name (Union[Unset, str]):
        notes (Union[Unset, str]): Owner-written, at most 2000 characters.
        region (Union[Unset, SiteRegion]): eu when created from the EU, EEA, UK or Switzerland.
        watches (Union[Unset, list['SiteWatchesItem']]):
    """

    brief: Union[Unset, str] = UNSET
    entities: Union[Unset, list["Entity"]] = UNSET
    id: Union[Unset, str] = UNSET
    memory_error: Union[None, Unset, str] = UNSET
    memory_rev: Union[Unset, int] = UNSET
    memory_updated_at: Union[None, Unset, datetime.datetime] = UNSET
    name: Union[Unset, str] = UNSET
    notes: Union[Unset, str] = UNSET
    region: Union[Unset, SiteRegion] = UNSET
    watches: Union[Unset, list["SiteWatchesItem"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        brief = self.brief

        entities: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.entities, Unset):
            entities = []
            for entities_item_data in self.entities:
                entities_item = entities_item_data.to_dict()
                entities.append(entities_item)

        id = self.id

        memory_error: Union[None, Unset, str]
        if isinstance(self.memory_error, Unset):
            memory_error = UNSET
        else:
            memory_error = self.memory_error

        memory_rev = self.memory_rev

        memory_updated_at: Union[None, Unset, str]
        if isinstance(self.memory_updated_at, Unset):
            memory_updated_at = UNSET
        elif isinstance(self.memory_updated_at, datetime.datetime):
            memory_updated_at = self.memory_updated_at.isoformat()
        else:
            memory_updated_at = self.memory_updated_at

        name = self.name

        notes = self.notes

        region: Union[Unset, str] = UNSET
        if not isinstance(self.region, Unset):
            region = self.region.value

        watches: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.watches, Unset):
            watches = []
            for watches_item_data in self.watches:
                watches_item = watches_item_data.to_dict()
                watches.append(watches_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if brief is not UNSET:
            field_dict["brief"] = brief
        if entities is not UNSET:
            field_dict["entities"] = entities
        if id is not UNSET:
            field_dict["id"] = id
        if memory_error is not UNSET:
            field_dict["memoryError"] = memory_error
        if memory_rev is not UNSET:
            field_dict["memoryRev"] = memory_rev
        if memory_updated_at is not UNSET:
            field_dict["memoryUpdatedAt"] = memory_updated_at
        if name is not UNSET:
            field_dict["name"] = name
        if notes is not UNSET:
            field_dict["notes"] = notes
        if region is not UNSET:
            field_dict["region"] = region
        if watches is not UNSET:
            field_dict["watches"] = watches

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.entity import Entity
        from ..models.site_watches_item import SiteWatchesItem

        d = dict(src_dict)
        brief = d.pop("brief", UNSET)

        entities = []
        _entities = d.pop("entities", UNSET)
        for entities_item_data in _entities or []:
            entities_item = Entity.from_dict(entities_item_data)

            entities.append(entities_item)

        id = d.pop("id", UNSET)

        def _parse_memory_error(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        memory_error = _parse_memory_error(d.pop("memoryError", UNSET))

        memory_rev = d.pop("memoryRev", UNSET)

        def _parse_memory_updated_at(
            data: object,
        ) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                memory_updated_at_type_0 = isoparse(data)

                return memory_updated_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        memory_updated_at = _parse_memory_updated_at(d.pop("memoryUpdatedAt", UNSET))

        name = d.pop("name", UNSET)

        notes = d.pop("notes", UNSET)

        _region = d.pop("region", UNSET)
        region: Union[Unset, SiteRegion]
        if isinstance(_region, Unset):
            region = UNSET
        else:
            region = SiteRegion(_region)

        watches = []
        _watches = d.pop("watches", UNSET)
        for watches_item_data in _watches or []:
            watches_item = SiteWatchesItem.from_dict(watches_item_data)

            watches.append(watches_item)

        site = cls(
            brief=brief,
            entities=entities,
            id=id,
            memory_error=memory_error,
            memory_rev=memory_rev,
            memory_updated_at=memory_updated_at,
            name=name,
            notes=notes,
            region=region,
            watches=watches,
        )

        site.additional_properties = d
        return site

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
