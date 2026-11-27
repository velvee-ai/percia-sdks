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

from ..models.update_watch_body_media import UpdateWatchBodyMedia
from ..models.update_watch_body_status import UpdateWatchBodyStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.update_watch_body_advanced import UpdateWatchBodyAdvanced
    from ..models.update_watch_body_notify_type_0 import UpdateWatchBodyNotifyType0
    from ..models.update_watch_body_notify_type_1 import UpdateWatchBodyNotifyType1


T = TypeVar("T", bound="UpdateWatchBody")


@_attrs_define
class UpdateWatchBody:
    """
    Attributes:
        acknowledge_unsupported (Union[Unset, bool]):
        advanced (Union[Unset, UpdateWatchBodyAdvanced]): Beta, only where recording is on (422 advanced_unavailable
            elsewhere): your own conditions. `conditions[]` are Condition objects {condition_id, kind
            (event|state|measurement), observable, role?: helper, while?/and_not?: {condition_id} or {signal: {signal, op,
            value}}, window_by?, window?, window_signal?, thresholds?: {..., trend, trend_window_s, trend_min_samples,
            trend_noise_floor, trend_slope}}. Example, alert if the belt stops while the motor is on:
            [{condition_id:"belt_stopped", kind:"state", observable:"the belt is not moving",
            while:{signal:{signal:"motor_running", op:"==", value:true}}}] (declare motor_running in the site's context
            first, and join the watch to that site with siteId). The source must be a Percia camera. See /docs/advanced.md.
        agent_id (Union[Unset, str]):
        agent_version (Union[None, Unset, int]):
        goal (Union[Unset, str]):
        media (Union[Unset, UpdateWatchBodyMedia]):
        notify (Union['UpdateWatchBodyNotifyType0', 'UpdateWatchBodyNotifyType1', Unset]):
        site_id (Union[None, Unset, str]):
        source_url (Union[Unset, str]):
        status (Union[Unset, UpdateWatchBodyStatus]):
        test_run (Union[Unset, bool]):
    """

    acknowledge_unsupported: Union[Unset, bool] = UNSET
    advanced: Union[Unset, "UpdateWatchBodyAdvanced"] = UNSET
    agent_id: Union[Unset, str] = UNSET
    agent_version: Union[None, Unset, int] = UNSET
    goal: Union[Unset, str] = UNSET
    media: Union[Unset, UpdateWatchBodyMedia] = UNSET
    notify: Union["UpdateWatchBodyNotifyType0", "UpdateWatchBodyNotifyType1", Unset] = UNSET
    site_id: Union[None, Unset, str] = UNSET
    source_url: Union[Unset, str] = UNSET
    status: Union[Unset, UpdateWatchBodyStatus] = UNSET
    test_run: Union[Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.update_watch_body_notify_type_0 import UpdateWatchBodyNotifyType0

        acknowledge_unsupported = self.acknowledge_unsupported

        advanced: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.advanced, Unset):
            advanced = self.advanced.to_dict()

        agent_id = self.agent_id

        agent_version: Union[None, Unset, int]
        if isinstance(self.agent_version, Unset):
            agent_version = UNSET
        else:
            agent_version = self.agent_version

        goal = self.goal

        media: Union[Unset, str] = UNSET
        if not isinstance(self.media, Unset):
            media = self.media.value

        notify: Union[Unset, dict[str, Any]]
        if isinstance(self.notify, Unset):
            notify = UNSET
        elif isinstance(self.notify, UpdateWatchBodyNotifyType0):
            notify = self.notify.to_dict()
        else:
            notify = self.notify.to_dict()

        site_id: Union[None, Unset, str]
        if isinstance(self.site_id, Unset):
            site_id = UNSET
        else:
            site_id = self.site_id

        source_url = self.source_url

        status: Union[Unset, str] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        test_run = self.test_run

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if acknowledge_unsupported is not UNSET:
            field_dict["acknowledgeUnsupported"] = acknowledge_unsupported
        if advanced is not UNSET:
            field_dict["advanced"] = advanced
        if agent_id is not UNSET:
            field_dict["agentId"] = agent_id
        if agent_version is not UNSET:
            field_dict["agentVersion"] = agent_version
        if goal is not UNSET:
            field_dict["goal"] = goal
        if media is not UNSET:
            field_dict["media"] = media
        if notify is not UNSET:
            field_dict["notify"] = notify
        if site_id is not UNSET:
            field_dict["siteId"] = site_id
        if source_url is not UNSET:
            field_dict["sourceUrl"] = source_url
        if status is not UNSET:
            field_dict["status"] = status
        if test_run is not UNSET:
            field_dict["testRun"] = test_run

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.update_watch_body_advanced import UpdateWatchBodyAdvanced
        from ..models.update_watch_body_notify_type_0 import UpdateWatchBodyNotifyType0
        from ..models.update_watch_body_notify_type_1 import UpdateWatchBodyNotifyType1

        d = dict(src_dict)
        acknowledge_unsupported = d.pop("acknowledgeUnsupported", UNSET)

        _advanced = d.pop("advanced", UNSET)
        advanced: Union[Unset, UpdateWatchBodyAdvanced]
        if isinstance(_advanced, Unset):
            advanced = UNSET
        else:
            advanced = UpdateWatchBodyAdvanced.from_dict(_advanced)

        agent_id = d.pop("agentId", UNSET)

        def _parse_agent_version(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        agent_version = _parse_agent_version(d.pop("agentVersion", UNSET))

        goal = d.pop("goal", UNSET)

        _media = d.pop("media", UNSET)
        media: Union[Unset, UpdateWatchBodyMedia]
        if isinstance(_media, Unset):
            media = UNSET
        else:
            media = UpdateWatchBodyMedia(_media)

        def _parse_notify(
            data: object,
        ) -> Union["UpdateWatchBodyNotifyType0", "UpdateWatchBodyNotifyType1", Unset]:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                notify_type_0 = UpdateWatchBodyNotifyType0.from_dict(data)

                return notify_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            notify_type_1 = UpdateWatchBodyNotifyType1.from_dict(data)

            return notify_type_1

        notify = _parse_notify(d.pop("notify", UNSET))

        def _parse_site_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        site_id = _parse_site_id(d.pop("siteId", UNSET))

        source_url = d.pop("sourceUrl", UNSET)

        _status = d.pop("status", UNSET)
        status: Union[Unset, UpdateWatchBodyStatus]
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = UpdateWatchBodyStatus(_status)

        test_run = d.pop("testRun", UNSET)

        update_watch_body = cls(
            acknowledge_unsupported=acknowledge_unsupported,
            advanced=advanced,
            agent_id=agent_id,
            agent_version=agent_version,
            goal=goal,
            media=media,
            notify=notify,
            site_id=site_id,
            source_url=source_url,
            status=status,
            test_run=test_run,
        )

        update_watch_body.additional_properties = d
        return update_watch_body

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
