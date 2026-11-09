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
    from ..models.agent_published_type_0 import AgentPublishedType0
    from ..models.agent_versions_item import AgentVersionsItem


T = TypeVar("T", bound="Agent")


@_attrs_define
class Agent:
    """
    Attributes:
        deployment_count (Union[Unset, int]):
        draft (Union[Unset, AgentConfig]): Up to 10 concerns plus a request budget. A zone is a polygon of 3 to 12 [x,
            y] points, each 0..1 (fractions of the frame).
        draft_changed (Union[Unset, bool]): True before the first publish, or when the draft differs from the published
            config.
        id (Union[Unset, str]):
        name (Union[Unset, str]):
        published (Union['AgentPublishedType0', None, Unset]): Config of the latest published version, null before the
            first publish.
        published_version (Union[None, Unset, int]):
        updated_at (Union[Unset, datetime.datetime]):
        versions (Union[Unset, list['AgentVersionsItem']]):
    """

    deployment_count: Union[Unset, int] = UNSET
    draft: Union[Unset, "AgentConfig"] = UNSET
    draft_changed: Union[Unset, bool] = UNSET
    id: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    published: Union["AgentPublishedType0", None, Unset] = UNSET
    published_version: Union[None, Unset, int] = UNSET
    updated_at: Union[Unset, datetime.datetime] = UNSET
    versions: Union[Unset, list["AgentVersionsItem"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.agent_published_type_0 import AgentPublishedType0

        deployment_count = self.deployment_count

        draft: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.draft, Unset):
            draft = self.draft.to_dict()

        draft_changed = self.draft_changed

        id = self.id

        name = self.name

        published: Union[None, Unset, dict[str, Any]]
        if isinstance(self.published, Unset):
            published = UNSET
        elif isinstance(self.published, AgentPublishedType0):
            published = self.published.to_dict()
        else:
            published = self.published

        published_version: Union[None, Unset, int]
        if isinstance(self.published_version, Unset):
            published_version = UNSET
        else:
            published_version = self.published_version

        updated_at: Union[Unset, str] = UNSET
        if not isinstance(self.updated_at, Unset):
            updated_at = self.updated_at.isoformat()

        versions: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.versions, Unset):
            versions = []
            for versions_item_data in self.versions:
                versions_item = versions_item_data.to_dict()
                versions.append(versions_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if deployment_count is not UNSET:
            field_dict["deploymentCount"] = deployment_count
        if draft is not UNSET:
            field_dict["draft"] = draft
        if draft_changed is not UNSET:
            field_dict["draftChanged"] = draft_changed
        if id is not UNSET:
            field_dict["id"] = id
        if name is not UNSET:
            field_dict["name"] = name
        if published is not UNSET:
            field_dict["published"] = published
        if published_version is not UNSET:
            field_dict["publishedVersion"] = published_version
        if updated_at is not UNSET:
            field_dict["updatedAt"] = updated_at
        if versions is not UNSET:
            field_dict["versions"] = versions

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.agent_config import AgentConfig
        from ..models.agent_published_type_0 import AgentPublishedType0
        from ..models.agent_versions_item import AgentVersionsItem

        d = dict(src_dict)
        deployment_count = d.pop("deploymentCount", UNSET)

        _draft = d.pop("draft", UNSET)
        draft: Union[Unset, AgentConfig]
        if isinstance(_draft, Unset):
            draft = UNSET
        else:
            draft = AgentConfig.from_dict(_draft)

        draft_changed = d.pop("draftChanged", UNSET)

        id = d.pop("id", UNSET)

        name = d.pop("name", UNSET)

        def _parse_published(data: object) -> Union["AgentPublishedType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                published_type_0 = AgentPublishedType0.from_dict(data)

                return published_type_0
            except:  # noqa: E722
                pass
            return cast(Union["AgentPublishedType0", None, Unset], data)

        published = _parse_published(d.pop("published", UNSET))

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

        versions = []
        _versions = d.pop("versions", UNSET)
        for versions_item_data in _versions or []:
            versions_item = AgentVersionsItem.from_dict(versions_item_data)

            versions.append(versions_item)

        agent = cls(
            deployment_count=deployment_count,
            draft=draft,
            draft_changed=draft_changed,
            id=id,
            name=name,
            published=published,
            published_version=published_version,
            updated_at=updated_at,
            versions=versions,
        )

        agent.additional_properties = d
        return agent

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
