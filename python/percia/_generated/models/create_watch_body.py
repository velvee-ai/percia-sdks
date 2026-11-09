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

from ..models.create_watch_body_media import CreateWatchBodyMedia
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.create_watch_body_notify_type_0 import CreateWatchBodyNotifyType0
    from ..models.create_watch_body_notify_type_1 import CreateWatchBodyNotifyType1


T = TypeVar("T", bound="CreateWatchBody")


@_attrs_define
class CreateWatchBody:
    """
    Attributes:
        source_url (str):
        agent_id (Union[Unset, str]):
        agent_version (Union[Unset, int]):
        destinations (Union[Unset, list[str]]):
        goal (Union[Unset, str]):
        media (Union[Unset, CreateWatchBodyMedia]):
        notify (Union['CreateWatchBodyNotifyType0', 'CreateWatchBodyNotifyType1', Unset]):
        site_id (Union[Unset, str]):
    """

    source_url: str
    agent_id: Union[Unset, str] = UNSET
    agent_version: Union[Unset, int] = UNSET
    destinations: Union[Unset, list[str]] = UNSET
    goal: Union[Unset, str] = UNSET
    media: Union[Unset, CreateWatchBodyMedia] = UNSET
    notify: Union["CreateWatchBodyNotifyType0", "CreateWatchBodyNotifyType1", Unset] = UNSET
    site_id: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.create_watch_body_notify_type_0 import CreateWatchBodyNotifyType0

        source_url: str
        source_url = self.source_url

        agent_id = self.agent_id

        agent_version = self.agent_version

        destinations: Union[Unset, list[str]] = UNSET
        if not isinstance(self.destinations, Unset):
            destinations = self.destinations

        goal = self.goal

        media: Union[Unset, str] = UNSET
        if not isinstance(self.media, Unset):
            media = self.media.value

        notify: Union[Unset, dict[str, Any]]
        if isinstance(self.notify, Unset):
            notify = UNSET
        elif isinstance(self.notify, CreateWatchBodyNotifyType0):
            notify = self.notify.to_dict()
        else:
            notify = self.notify.to_dict()

        site_id = self.site_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "sourceUrl": source_url,
            }
        )
        if agent_id is not UNSET:
            field_dict["agentId"] = agent_id
        if agent_version is not UNSET:
            field_dict["agentVersion"] = agent_version
        if destinations is not UNSET:
            field_dict["destinations"] = destinations
        if goal is not UNSET:
            field_dict["goal"] = goal
        if media is not UNSET:
            field_dict["media"] = media
        if notify is not UNSET:
            field_dict["notify"] = notify
        if site_id is not UNSET:
            field_dict["siteId"] = site_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.create_watch_body_notify_type_0 import CreateWatchBodyNotifyType0
        from ..models.create_watch_body_notify_type_1 import CreateWatchBodyNotifyType1

        d = dict(src_dict)

        def _parse_source_url(data: object) -> str:
            return cast(str, data)

        source_url = _parse_source_url(d.pop("sourceUrl"))

        agent_id = d.pop("agentId", UNSET)

        agent_version = d.pop("agentVersion", UNSET)

        destinations = cast(list[str], d.pop("destinations", UNSET))

        goal = d.pop("goal", UNSET)

        _media = d.pop("media", UNSET)
        media: Union[Unset, CreateWatchBodyMedia]
        if isinstance(_media, Unset):
            media = UNSET
        else:
            media = CreateWatchBodyMedia(_media)

        def _parse_notify(
            data: object,
        ) -> Union["CreateWatchBodyNotifyType0", "CreateWatchBodyNotifyType1", Unset]:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                notify_type_0 = CreateWatchBodyNotifyType0.from_dict(data)

                return notify_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            notify_type_1 = CreateWatchBodyNotifyType1.from_dict(data)

            return notify_type_1

        notify = _parse_notify(d.pop("notify", UNSET))

        site_id = d.pop("siteId", UNSET)

        create_watch_body = cls(
            source_url=source_url,
            agent_id=agent_id,
            agent_version=agent_version,
            destinations=destinations,
            goal=goal,
            media=media,
            notify=notify,
            site_id=site_id,
        )

        create_watch_body.additional_properties = d
        return create_watch_body

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
