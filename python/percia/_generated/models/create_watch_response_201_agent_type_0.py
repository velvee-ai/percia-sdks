from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
    cast,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateWatchResponse201AgentType0")


@_attrs_define
class CreateWatchResponse201AgentType0:
    """Only on watches deployed with an agent. version is the one it runs; followsLatest is true when it was not pinned.

    Attributes:
        follows_latest (Union[Unset, bool]):
        id (Union[Unset, str]):
        name (Union[Unset, str]):
        version (Union[None, Unset, int]):
    """

    follows_latest: Union[Unset, bool] = UNSET
    id: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    version: Union[None, Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        follows_latest = self.follows_latest

        id = self.id

        name = self.name

        version: Union[None, Unset, int]
        if isinstance(self.version, Unset):
            version = UNSET
        else:
            version = self.version

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if follows_latest is not UNSET:
            field_dict["followsLatest"] = follows_latest
        if id is not UNSET:
            field_dict["id"] = id
        if name is not UNSET:
            field_dict["name"] = name
        if version is not UNSET:
            field_dict["version"] = version

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        follows_latest = d.pop("followsLatest", UNSET)

        id = d.pop("id", UNSET)

        name = d.pop("name", UNSET)

        def _parse_version(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        version = _parse_version(d.pop("version", UNSET))

        create_watch_response_201_agent_type_0 = cls(
            follows_latest=follows_latest,
            id=id,
            name=name,
            version=version,
        )

        create_watch_response_201_agent_type_0.additional_properties = d
        return create_watch_response_201_agent_type_0

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
