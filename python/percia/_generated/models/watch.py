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

from ..models.watch_core_state import WatchCoreState
from ..models.watch_display_status import WatchDisplayStatus
from ..models.watch_last_delivery_type_1 import WatchLastDeliveryType1
from ..models.watch_runtime import WatchRuntime
from ..models.watch_source_type import WatchSourceType
from ..models.watch_status import WatchStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.watch_agent_type_0 import WatchAgentType0
    from ..models.watch_camera_type_0 import WatchCameraType0
    from ..models.watch_last_event_type_0 import WatchLastEventType0
    from ..models.watch_notify import WatchNotify
    from ..models.watch_site_type_0 import WatchSiteType0


T = TypeVar("T", bound="Watch")


@_attrs_define
class Watch:
    """
    Attributes:
        agent (Union['WatchAgentType0', None, Unset]): Only on watches deployed with an agent. version is the one it
            runs; followsLatest is true when it was not pinned.
        camera (Union['WatchCameraType0', None, Unset]): Only on phone-camera watches.
        core_state (Union[Unset, WatchCoreState]): Only on core watches. running is judging; absent is paused (nothing
            runs on Percia core); off means the core switch was off when it was created; error: see syncError.
        created_at (Union[Unset, datetime.datetime]):
        display_status (Union[Unset, WatchDisplayStatus]): Needs attention when syncError is set, the last delivery
            failed, a rule of the watch points at a broken integration, or an active watch gets no video (noVideoSince set).
        event_count (Union[Unset, int]):
        goal (Union[Unset, str]): For a deployed watch, the agent's name.
        id (Union[Unset, str]):
        last_delivery (Union[None, Unset, WatchLastDeliveryType1]): Status of the newest event that is not pending.
            displayStatus comes from this, so a pending event does not hide a failed one.
        last_event (Union['WatchLastEventType0', None, Unset]):
        no_video_since (Union[None, Unset, datetime.datetime]): When the camera stopped sending video, else null. An
            active watch is paused automatically 60 minutes after this time (pausedReason no_video). Kept on a no_video
            pause; cleared on resume.
        notify (Union[Unset, WatchNotify]):
        paused_reason (Union[None, Unset, str]): Why a paused watch is paused: user (paused by the owner or an agent, or
            an older pause with no recorded reason), no_video (paused automatically after 60 minutes without video from the
            camera), needs_billing (free minutes and credits used, no card), spend_cap (the monthly cap was reached),
            payment_failed (a payment failed and the 48-hour grace is over; resumes by itself when the payment succeeds) or
            ended (a short-term watch reached its end). Resume with PATCH status active.
        runtime (Union[Unset, WatchRuntime]): Where the watch is judged: pool (default) or core (Percia core, Percept
            Cloud). Fixed when the watch is created.
        site (Union['WatchSiteType0', None, Unset]): The site this watch belongs to (shared memory), else null.
        source_type (Union[Unset, WatchSourceType]): phone = a paired phone or laptop camera; sourceUrl is then percia-
            cam://<cameraId>.
        source_url (Union[Unset, str]): Credentials are redacted.
        status (Union[Unset, WatchStatus]):
        sync_error (Union[None, Unset, str]):
        synced_at (Union[None, Unset, datetime.datetime]):
    """

    agent: Union["WatchAgentType0", None, Unset] = UNSET
    camera: Union["WatchCameraType0", None, Unset] = UNSET
    core_state: Union[Unset, WatchCoreState] = UNSET
    created_at: Union[Unset, datetime.datetime] = UNSET
    display_status: Union[Unset, WatchDisplayStatus] = UNSET
    event_count: Union[Unset, int] = UNSET
    goal: Union[Unset, str] = UNSET
    id: Union[Unset, str] = UNSET
    last_delivery: Union[None, Unset, WatchLastDeliveryType1] = UNSET
    last_event: Union["WatchLastEventType0", None, Unset] = UNSET
    no_video_since: Union[None, Unset, datetime.datetime] = UNSET
    notify: Union[Unset, "WatchNotify"] = UNSET
    paused_reason: Union[None, Unset, str] = UNSET
    runtime: Union[Unset, WatchRuntime] = UNSET
    site: Union["WatchSiteType0", None, Unset] = UNSET
    source_type: Union[Unset, WatchSourceType] = UNSET
    source_url: Union[Unset, str] = UNSET
    status: Union[Unset, WatchStatus] = UNSET
    sync_error: Union[None, Unset, str] = UNSET
    synced_at: Union[None, Unset, datetime.datetime] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.watch_agent_type_0 import WatchAgentType0
        from ..models.watch_camera_type_0 import WatchCameraType0
        from ..models.watch_last_event_type_0 import WatchLastEventType0
        from ..models.watch_site_type_0 import WatchSiteType0

        agent: Union[None, Unset, dict[str, Any]]
        if isinstance(self.agent, Unset):
            agent = UNSET
        elif isinstance(self.agent, WatchAgentType0):
            agent = self.agent.to_dict()
        else:
            agent = self.agent

        camera: Union[None, Unset, dict[str, Any]]
        if isinstance(self.camera, Unset):
            camera = UNSET
        elif isinstance(self.camera, WatchCameraType0):
            camera = self.camera.to_dict()
        else:
            camera = self.camera

        core_state: Union[Unset, str] = UNSET
        if not isinstance(self.core_state, Unset):
            core_state = self.core_state.value

        created_at: Union[Unset, str] = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()

        display_status: Union[Unset, str] = UNSET
        if not isinstance(self.display_status, Unset):
            display_status = self.display_status.value

        event_count = self.event_count

        goal = self.goal

        id = self.id

        last_delivery: Union[None, Unset, str]
        if isinstance(self.last_delivery, Unset):
            last_delivery = UNSET
        elif isinstance(self.last_delivery, WatchLastDeliveryType1):
            last_delivery = self.last_delivery.value
        else:
            last_delivery = self.last_delivery

        last_event: Union[None, Unset, dict[str, Any]]
        if isinstance(self.last_event, Unset):
            last_event = UNSET
        elif isinstance(self.last_event, WatchLastEventType0):
            last_event = self.last_event.to_dict()
        else:
            last_event = self.last_event

        no_video_since: Union[None, Unset, str]
        if isinstance(self.no_video_since, Unset):
            no_video_since = UNSET
        elif isinstance(self.no_video_since, datetime.datetime):
            no_video_since = self.no_video_since.isoformat()
        else:
            no_video_since = self.no_video_since

        notify: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.notify, Unset):
            notify = self.notify.to_dict()

        paused_reason: Union[None, Unset, str]
        if isinstance(self.paused_reason, Unset):
            paused_reason = UNSET
        else:
            paused_reason = self.paused_reason

        runtime: Union[Unset, str] = UNSET
        if not isinstance(self.runtime, Unset):
            runtime = self.runtime.value

        site: Union[None, Unset, dict[str, Any]]
        if isinstance(self.site, Unset):
            site = UNSET
        elif isinstance(self.site, WatchSiteType0):
            site = self.site.to_dict()
        else:
            site = self.site

        source_type: Union[Unset, str] = UNSET
        if not isinstance(self.source_type, Unset):
            source_type = self.source_type.value

        source_url = self.source_url

        status: Union[Unset, str] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        sync_error: Union[None, Unset, str]
        if isinstance(self.sync_error, Unset):
            sync_error = UNSET
        else:
            sync_error = self.sync_error

        synced_at: Union[None, Unset, str]
        if isinstance(self.synced_at, Unset):
            synced_at = UNSET
        elif isinstance(self.synced_at, datetime.datetime):
            synced_at = self.synced_at.isoformat()
        else:
            synced_at = self.synced_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if agent is not UNSET:
            field_dict["agent"] = agent
        if camera is not UNSET:
            field_dict["camera"] = camera
        if core_state is not UNSET:
            field_dict["coreState"] = core_state
        if created_at is not UNSET:
            field_dict["createdAt"] = created_at
        if display_status is not UNSET:
            field_dict["displayStatus"] = display_status
        if event_count is not UNSET:
            field_dict["eventCount"] = event_count
        if goal is not UNSET:
            field_dict["goal"] = goal
        if id is not UNSET:
            field_dict["id"] = id
        if last_delivery is not UNSET:
            field_dict["lastDelivery"] = last_delivery
        if last_event is not UNSET:
            field_dict["lastEvent"] = last_event
        if no_video_since is not UNSET:
            field_dict["noVideoSince"] = no_video_since
        if notify is not UNSET:
            field_dict["notify"] = notify
        if paused_reason is not UNSET:
            field_dict["pausedReason"] = paused_reason
        if runtime is not UNSET:
            field_dict["runtime"] = runtime
        if site is not UNSET:
            field_dict["site"] = site
        if source_type is not UNSET:
            field_dict["sourceType"] = source_type
        if source_url is not UNSET:
            field_dict["sourceUrl"] = source_url
        if status is not UNSET:
            field_dict["status"] = status
        if sync_error is not UNSET:
            field_dict["syncError"] = sync_error
        if synced_at is not UNSET:
            field_dict["syncedAt"] = synced_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.watch_agent_type_0 import WatchAgentType0
        from ..models.watch_camera_type_0 import WatchCameraType0
        from ..models.watch_last_event_type_0 import WatchLastEventType0
        from ..models.watch_notify import WatchNotify
        from ..models.watch_site_type_0 import WatchSiteType0

        d = dict(src_dict)

        def _parse_agent(data: object) -> Union["WatchAgentType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                agent_type_0 = WatchAgentType0.from_dict(data)

                return agent_type_0
            except:  # noqa: E722
                pass
            return cast(Union["WatchAgentType0", None, Unset], data)

        agent = _parse_agent(d.pop("agent", UNSET))

        def _parse_camera(data: object) -> Union["WatchCameraType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                camera_type_0 = WatchCameraType0.from_dict(data)

                return camera_type_0
            except:  # noqa: E722
                pass
            return cast(Union["WatchCameraType0", None, Unset], data)

        camera = _parse_camera(d.pop("camera", UNSET))

        _core_state = d.pop("coreState", UNSET)
        core_state: Union[Unset, WatchCoreState]
        if isinstance(_core_state, Unset):
            core_state = UNSET
        else:
            core_state = WatchCoreState(_core_state)

        _created_at = d.pop("createdAt", UNSET)
        created_at: Union[Unset, datetime.datetime]
        if isinstance(_created_at, Unset):
            created_at = UNSET
        else:
            created_at = isoparse(_created_at)

        _display_status = d.pop("displayStatus", UNSET)
        display_status: Union[Unset, WatchDisplayStatus]
        if isinstance(_display_status, Unset):
            display_status = UNSET
        else:
            display_status = WatchDisplayStatus(_display_status)

        event_count = d.pop("eventCount", UNSET)

        goal = d.pop("goal", UNSET)

        id = d.pop("id", UNSET)

        def _parse_last_delivery(
            data: object,
        ) -> Union[None, Unset, WatchLastDeliveryType1]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                last_delivery_type_1 = WatchLastDeliveryType1(data)

                return last_delivery_type_1
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, WatchLastDeliveryType1], data)

        last_delivery = _parse_last_delivery(d.pop("lastDelivery", UNSET))

        def _parse_last_event(
            data: object,
        ) -> Union["WatchLastEventType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                last_event_type_0 = WatchLastEventType0.from_dict(data)

                return last_event_type_0
            except:  # noqa: E722
                pass
            return cast(Union["WatchLastEventType0", None, Unset], data)

        last_event = _parse_last_event(d.pop("lastEvent", UNSET))

        def _parse_no_video_since(
            data: object,
        ) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                no_video_since_type_0 = isoparse(data)

                return no_video_since_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        no_video_since = _parse_no_video_since(d.pop("noVideoSince", UNSET))

        _notify = d.pop("notify", UNSET)
        notify: Union[Unset, WatchNotify]
        if isinstance(_notify, Unset):
            notify = UNSET
        else:
            notify = WatchNotify.from_dict(_notify)

        def _parse_paused_reason(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        paused_reason = _parse_paused_reason(d.pop("pausedReason", UNSET))

        _runtime = d.pop("runtime", UNSET)
        runtime: Union[Unset, WatchRuntime]
        if isinstance(_runtime, Unset):
            runtime = UNSET
        else:
            runtime = WatchRuntime(_runtime)

        def _parse_site(data: object) -> Union["WatchSiteType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                site_type_0 = WatchSiteType0.from_dict(data)

                return site_type_0
            except:  # noqa: E722
                pass
            return cast(Union["WatchSiteType0", None, Unset], data)

        site = _parse_site(d.pop("site", UNSET))

        _source_type = d.pop("sourceType", UNSET)
        source_type: Union[Unset, WatchSourceType]
        if isinstance(_source_type, Unset):
            source_type = UNSET
        else:
            source_type = WatchSourceType(_source_type)

        source_url = d.pop("sourceUrl", UNSET)

        _status = d.pop("status", UNSET)
        status: Union[Unset, WatchStatus]
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = WatchStatus(_status)

        def _parse_sync_error(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        sync_error = _parse_sync_error(d.pop("syncError", UNSET))

        def _parse_synced_at(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                synced_at_type_0 = isoparse(data)

                return synced_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        synced_at = _parse_synced_at(d.pop("syncedAt", UNSET))

        watch = cls(
            agent=agent,
            camera=camera,
            core_state=core_state,
            created_at=created_at,
            display_status=display_status,
            event_count=event_count,
            goal=goal,
            id=id,
            last_delivery=last_delivery,
            last_event=last_event,
            no_video_since=no_video_since,
            notify=notify,
            paused_reason=paused_reason,
            runtime=runtime,
            site=site,
            source_type=source_type,
            source_url=source_url,
            status=status,
            sync_error=sync_error,
            synced_at=synced_at,
        )

        watch.additional_properties = d
        return watch

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
