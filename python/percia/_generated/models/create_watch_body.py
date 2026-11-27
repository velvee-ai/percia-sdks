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
    from ..models.create_watch_body_advanced import CreateWatchBodyAdvanced
    from ..models.create_watch_body_notify_type_0 import CreateWatchBodyNotifyType0
    from ..models.create_watch_body_notify_type_1 import CreateWatchBodyNotifyType1


T = TypeVar("T", bound="CreateWatchBody")


@_attrs_define
class CreateWatchBody:
    """
    Attributes:
        source_url (str):
        acknowledge_unsupported (Union[Unset, bool]):
        advanced (Union[Unset, CreateWatchBodyAdvanced]): Beta, only where recording is on (422 advanced_unavailable
            elsewhere): your own conditions. `conditions[]` are Condition objects {condition_id, kind
            (event|state|measurement), observable, role?: helper, while?/and_not?: {condition_id} or {signal: {signal, op,
            value}}, window_by?, window?, window_signal?, thresholds?: {..., trend, trend_window_s, trend_min_samples,
            trend_noise_floor, trend_slope}}. Example, alert if the belt stops while the motor is on:
            [{condition_id:"belt_stopped", kind:"state", observable:"the belt is not moving",
            while:{signal:{signal:"motor_running", op:"==", value:true}}}] (declare motor_running in the site's context
            first, and join the watch to that site with siteId). The source must be a Percia camera. See /docs/advanced.md.
        agent_id (Union[Unset, str]):
        agent_version (Union[Unset, int]):
        destinations (Union[Unset, list[str]]):
        draft_id (Union[Unset, str]):
        goal (Union[Unset, str]):
        media (Union[Unset, CreateWatchBodyMedia]):
        notify (Union['CreateWatchBodyNotifyType0', 'CreateWatchBodyNotifyType1', Unset]):
        site_id (Union[Unset, str]):
        start_paused (Union[Unset, bool]):
    """

    source_url: str
    acknowledge_unsupported: Union[Unset, bool] = UNSET
    advanced: Union[Unset, "CreateWatchBodyAdvanced"] = UNSET
    agent_id: Union[Unset, str] = UNSET
    agent_version: Union[Unset, int] = UNSET
    destinations: Union[Unset, list[str]] = UNSET
    draft_id: Union[Unset, str] = UNSET
    goal: Union[Unset, str] = UNSET
    media: Union[Unset, CreateWatchBodyMedia] = UNSET
    notify: Union["CreateWatchBodyNotifyType0", "CreateWatchBodyNotifyType1", Unset] = UNSET
    site_id: Union[Unset, str] = UNSET
    start_paused: Union[Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.create_watch_body_notify_type_0 import CreateWatchBodyNotifyType0

        source_url = self.source_url

        acknowledge_unsupported = self.acknowledge_unsupported

        advanced: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.advanced, Unset):
            advanced = self.advanced.to_dict()

        agent_id = self.agent_id

        agent_version = self.agent_version

        destinations: Union[Unset, list[str]] = UNSET
        if not isinstance(self.destinations, Unset):
            destinations = self.destinations

        draft_id = self.draft_id

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

        start_paused = self.start_paused

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "sourceUrl": source_url,
            }
        )
        if acknowledge_unsupported is not UNSET:
            field_dict["acknowledgeUnsupported"] = acknowledge_unsupported
        if advanced is not UNSET:
            field_dict["advanced"] = advanced
        if agent_id is not UNSET:
            field_dict["agentId"] = agent_id
        if agent_version is not UNSET:
            field_dict["agentVersion"] = agent_version
        if destinations is not UNSET:
            field_dict["destinations"] = destinations
        if draft_id is not UNSET:
            field_dict["draftId"] = draft_id
        if goal is not UNSET:
            field_dict["goal"] = goal
        if media is not UNSET:
            field_dict["media"] = media
        if notify is not UNSET:
            field_dict["notify"] = notify
        if site_id is not UNSET:
            field_dict["siteId"] = site_id
        if start_paused is not UNSET:
            field_dict["startPaused"] = start_paused

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.create_watch_body_advanced import CreateWatchBodyAdvanced
        from ..models.create_watch_body_notify_type_0 import CreateWatchBodyNotifyType0
        from ..models.create_watch_body_notify_type_1 import CreateWatchBodyNotifyType1

        d = dict(src_dict)
        source_url = d.pop("sourceUrl")

        acknowledge_unsupported = d.pop("acknowledgeUnsupported", UNSET)

        _advanced = d.pop("advanced", UNSET)
        advanced: Union[Unset, CreateWatchBodyAdvanced]
        if isinstance(_advanced, Unset):
            advanced = UNSET
        else:
            advanced = CreateWatchBodyAdvanced.from_dict(_advanced)

        agent_id = d.pop("agentId", UNSET)

        agent_version = d.pop("agentVersion", UNSET)

        destinations = cast(list[str], d.pop("destinations", UNSET))

        draft_id = d.pop("draftId", UNSET)

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

        start_paused = d.pop("startPaused", UNSET)

        create_watch_body = cls(
            source_url=source_url,
            acknowledge_unsupported=acknowledge_unsupported,
            advanced=advanced,
            agent_id=agent_id,
            agent_version=agent_version,
            destinations=destinations,
            draft_id=draft_id,
            goal=goal,
            media=media,
            notify=notify,
            site_id=site_id,
            start_paused=start_paused,
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
