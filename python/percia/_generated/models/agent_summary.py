import datetime
from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
    cast,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="AgentSummary")


@_attrs_define
class AgentSummary:
    """
    Attributes:
        deployment_count (Union[Unset, int]):
        draft_changed (Union[Unset, bool]): True before the first publish, or when the draft differs from the published
            config.
        id (Union[Unset, str]):
        name (Union[Unset, str]):
        published_version (Union[None, Unset, int]):
        updated_at (Union[Unset, datetime.datetime]):
    """

    deployment_count: Union[Unset, int] = UNSET
    draft_changed: Union[Unset, bool] = UNSET
    id: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    published_version: Union[None, Unset, int] = UNSET
    updated_at: Union[Unset, datetime.datetime] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        deployment_count = self.deployment_count

        draft_changed = self.draft_changed

        id = self.id

        name = self.name

        published_version: Union[None, Unset, int]
        if isinstance(self.published_version, Unset):
            published_version = UNSET
        else:
            published_version = self.published_version

        updated_at: Union[Unset, str] = UNSET
        if not isinstance(self.updated_at, Unset):
            updated_at = self.updated_at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if deployment_count is not UNSET:
            field_dict["deploymentCount"] = deployment_count
        if draft_changed is not UNSET:
            field_dict["draftChanged"] = draft_changed
        if id is not UNSET:
            field_dict["id"] = id
        if name is not UNSET:
            field_dict["name"] = name
        if published_version is not UNSET:
            field_dict["publishedVersion"] = published_version
        if updated_at is not UNSET:
            field_dict["updatedAt"] = updated_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        deployment_count = d.pop("deploymentCount", UNSET)

        draft_changed = d.pop("draftChanged", UNSET)

        id = d.pop("id", UNSET)

        name = d.pop("name", UNSET)

        def _parse_published_version(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        published_version = _parse_published_version(d.pop("publishedVersion", UNSET))

        _updated_at = d.pop("updatedAt", UNSET)
        updated_at: Union[Unset, datetime.datetime]
        if isinstance(_updated_at, Unset):
            updated_at = UNSET
        else:
            updated_at = isoparse(_updated_at)

        agent_summary = cls(
            deployment_count=deployment_count,
            draft_changed=draft_changed,
            id=id,
            name=name,
            published_version=published_version,
            updated_at=updated_at,
        )

        agent_summary.additional_properties = d
        return agent_summary

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
