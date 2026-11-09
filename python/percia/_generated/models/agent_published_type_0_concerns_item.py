from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
    cast,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.agent_published_type_0_concerns_item_kind import (
    AgentPublishedType0ConcernsItemKind,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="AgentPublishedType0ConcernsItem")


@_attrs_define
class AgentPublishedType0ConcernsItem:
    """
    Attributes:
        id (str): Slug, at most 32 characters, unique within the agent.
        kind (AgentPublishedType0ConcernsItemKind):
        text (str): 5 to 500 characters.
        cooldown_s (Union[Unset, int]):
        exclude_zones (Union[Unset, list[list[list[float]]]]):
        ignore (Union[Unset, list[str]]):
        min_confidence (Union[Unset, float]):
        rearm_s (Union[Unset, int]):
        recheck_s (Union[Unset, int]):
        zones (Union[Unset, list[list[list[float]]]]):
    """

    id: str
    kind: AgentPublishedType0ConcernsItemKind
    text: str
    cooldown_s: Union[Unset, int] = UNSET
    exclude_zones: Union[Unset, list[list[list[float]]]] = UNSET
    ignore: Union[Unset, list[str]] = UNSET
    min_confidence: Union[Unset, float] = UNSET
    rearm_s: Union[Unset, int] = UNSET
    recheck_s: Union[Unset, int] = UNSET
    zones: Union[Unset, list[list[list[float]]]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        kind = self.kind.value

        text = self.text

        cooldown_s = self.cooldown_s

        exclude_zones: Union[Unset, list[list[list[float]]]] = UNSET
        if not isinstance(self.exclude_zones, Unset):
            exclude_zones = []
            for exclude_zones_item_data in self.exclude_zones:
                exclude_zones_item = []
                for exclude_zones_item_item_data in exclude_zones_item_data:
                    exclude_zones_item_item = exclude_zones_item_item_data

                    exclude_zones_item.append(exclude_zones_item_item)

                exclude_zones.append(exclude_zones_item)

        ignore: Union[Unset, list[str]] = UNSET
        if not isinstance(self.ignore, Unset):
            ignore = self.ignore

        min_confidence = self.min_confidence

        rearm_s = self.rearm_s

        recheck_s = self.recheck_s

        zones: Union[Unset, list[list[list[float]]]] = UNSET
        if not isinstance(self.zones, Unset):
            zones = []
            for zones_item_data in self.zones:
                zones_item = []
                for zones_item_item_data in zones_item_data:
                    zones_item_item = zones_item_item_data

                    zones_item.append(zones_item_item)

                zones.append(zones_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "kind": kind,
                "text": text,
            }
        )
        if cooldown_s is not UNSET:
            field_dict["cooldownS"] = cooldown_s
        if exclude_zones is not UNSET:
            field_dict["excludeZones"] = exclude_zones
        if ignore is not UNSET:
            field_dict["ignore"] = ignore
        if min_confidence is not UNSET:
            field_dict["minConfidence"] = min_confidence
        if rearm_s is not UNSET:
            field_dict["rearmS"] = rearm_s
        if recheck_s is not UNSET:
            field_dict["recheckS"] = recheck_s
        if zones is not UNSET:
            field_dict["zones"] = zones

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        kind = AgentPublishedType0ConcernsItemKind(d.pop("kind"))

        text = d.pop("text")

        cooldown_s = d.pop("cooldownS", UNSET)

        exclude_zones = []
        _exclude_zones = d.pop("excludeZones", UNSET)
        for exclude_zones_item_data in _exclude_zones or []:
            exclude_zones_item = []
            _exclude_zones_item = exclude_zones_item_data
            for exclude_zones_item_item_data in _exclude_zones_item:
                exclude_zones_item_item = cast(list[float], exclude_zones_item_item_data)

                exclude_zones_item.append(exclude_zones_item_item)

            exclude_zones.append(exclude_zones_item)

        ignore = cast(list[str], d.pop("ignore", UNSET))

        min_confidence = d.pop("minConfidence", UNSET)

        rearm_s = d.pop("rearmS", UNSET)

        recheck_s = d.pop("recheckS", UNSET)

        zones = []
        _zones = d.pop("zones", UNSET)
        for zones_item_data in _zones or []:
            zones_item = []
            _zones_item = zones_item_data
            for zones_item_item_data in _zones_item:
                zones_item_item = cast(list[float], zones_item_item_data)

                zones_item.append(zones_item_item)

            zones.append(zones_item)

        agent_published_type_0_concerns_item = cls(
            id=id,
            kind=kind,
            text=text,
            cooldown_s=cooldown_s,
            exclude_zones=exclude_zones,
            ignore=ignore,
            min_confidence=min_confidence,
            rearm_s=rearm_s,
            recheck_s=recheck_s,
            zones=zones,
        )

        agent_published_type_0_concerns_item.additional_properties = d
        return agent_published_type_0_concerns_item

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
