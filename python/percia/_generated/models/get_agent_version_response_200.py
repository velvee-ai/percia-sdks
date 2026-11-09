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

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.agent_config import AgentConfig


T = TypeVar("T", bound="GetAgentVersionResponse200")


@_attrs_define
class GetAgentVersionResponse200:
    """
    Attributes:
        config (Union[Unset, AgentConfig]): Up to 10 concerns plus a request budget. A zone is a polygon of 3 to 12 [x,
            y] points, each 0..1 (fractions of the frame).
        created_at (Union[Unset, datetime.datetime]):
        note (Union[None, Unset, str]):
        version (Union[Unset, int]):
    """

    config: Union[Unset, "AgentConfig"] = UNSET
    created_at: Union[Unset, datetime.datetime] = UNSET
    note: Union[None, Unset, str] = UNSET
    version: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        config: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.config, Unset):
            config = self.config.to_dict()

        created_at: Union[Unset, str] = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()

        note: Union[None, Unset, str]
        if isinstance(self.note, Unset):
            note = UNSET
        else:
            note = self.note

        version = self.version

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if config is not UNSET:
            field_dict["config"] = config
        if created_at is not UNSET:
            field_dict["createdAt"] = created_at
        if note is not UNSET:
            field_dict["note"] = note
        if version is not UNSET:
            field_dict["version"] = version

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.agent_config import AgentConfig

        d = dict(src_dict)
        _config = d.pop("config", UNSET)
        config: Union[Unset, AgentConfig]
        if isinstance(_config, Unset):
            config = UNSET
        else:
            config = AgentConfig.from_dict(_config)

        _created_at = d.pop("createdAt", UNSET)
        created_at: Union[Unset, datetime.datetime]
        if isinstance(_created_at, Unset):
            created_at = UNSET
        else:
            created_at = isoparse(_created_at)

        def _parse_note(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        note = _parse_note(d.pop("note", UNSET))

        version = d.pop("version", UNSET)

        get_agent_version_response_200 = cls(
            config=config,
            created_at=created_at,
            note=note,
            version=version,
        )

        get_agent_version_response_200.additional_properties = d
        return get_agent_version_response_200

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
