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

from ..models.get_watch_response_200_core_state import GetWatchResponse200CoreState
from ..models.get_watch_response_200_display_status import (
    GetWatchResponse200DisplayStatus,
)
from ..models.get_watch_response_200_last_delivery_type_1 import (
    GetWatchResponse200LastDeliveryType1,
)
from ..models.get_watch_response_200_runtime import GetWatchResponse200Runtime
from ..models.get_watch_response_200_source_type import GetWatchResponse200SourceType
from ..models.get_watch_response_200_status import GetWatchResponse200Status
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.get_watch_response_200_agent_type_0 import (
        GetWatchResponse200AgentType0,
    )
    from ..models.get_watch_response_200_camera_type_0 import (
        GetWatchResponse200CameraType0,
    )
    from ..models.get_watch_response_200_engine_type_0 import (
        GetWatchResponse200EngineType0,
    )
    from ..models.get_watch_response_200_last_event_type_0 import (
        GetWatchResponse200LastEventType0,
    )
    from ..models.get_watch_response_200_notify import GetWatchResponse200Notify
    from ..models.get_watch_response_200_site_type_0 import GetWatchResponse200SiteType0


T = TypeVar("T", bound="GetWatchResponse200")


@_attrs_define
class GetWatchResponse200:
    """
    Attributes:
        agent (Union['GetWatchResponse200AgentType0', None, Unset]): Only on watches deployed with an agent. version is
            the one it runs; followsLatest is true when it was not pinned.
        camera (Union['GetWatchResponse200CameraType0', None, Unset]): Only on phone-camera watches.
        core_state (Union[Unset, GetWatchResponse200CoreState]): Only on core watches. running is judging; absent is
            paused (nothing runs on Percia core); off means the core switch was off when it was created; error: see
            syncError.
        created_at (Union[Unset, datetime.datetime]):
        display_status (Union[Unset, GetWatchResponse200DisplayStatus]): Needs attention when syncError is set, the last
            delivery failed, a rule of the watch points at a broken integration, or an active watch gets no video
            (noVideoSince set).
        engine (Union['GetWatchResponse200EngineType0', None, Unset]): The engine release (Percept version plus Percia's
            runner revision) that judges this watch, or would when it is active. pinned is true when support fixed it for
            this watch; otherwise it follows Percia's staged rollout. Null while none is assigned. Informational: there is
            nothing to set.
        event_count (Union[Unset, int]):
        goal (Union[Unset, str]): For a deployed watch, the agent's name.
        id (Union[Unset, str]):
        last_delivery (Union[GetWatchResponse200LastDeliveryType1, None, Unset]): Status of the newest event that is not
            pending. displayStatus comes from this, so a pending event does not hide a failed one.
        last_event (Union['GetWatchResponse200LastEventType0', None, Unset]):
        no_video_since (Union[None, Unset, datetime.datetime]): When the camera stopped sending video, else null. An
            active watch is paused automatically 60 minutes after this time (pausedReason no_video). Kept on a no_video
            pause; cleared on resume.
        notify (Union[Unset, GetWatchResponse200Notify]):
        paused_reason (Union[None, Unset, str]): Why a paused watch is paused: user (paused by the owner or an agent, or
            an older pause with no recorded reason), no_video (paused automatically after 60 minutes without video from the
            camera), needs_billing (free minutes and credits used, no card), spend_cap (the monthly cap was reached),
            payment_failed (a payment failed and the 48-hour grace is over; resumes by itself when the payment succeeds) or
            ended (a short-term watch reached its end). Resume with PATCH status active.
        runtime (Union[Unset, GetWatchResponse200Runtime]): Where the watch is judged: pool (default) or core (Percia
            core, Percept Cloud). Fixed when the watch is created.
        secret_hint (Union[None, Unset, str]):
        site (Union['GetWatchResponse200SiteType0', None, Unset]): The site this watch belongs to (shared memory), else
            null.
        source_type (Union[Unset, GetWatchResponse200SourceType]): phone = a paired phone or laptop camera; sourceUrl is
            then percia-cam://<cameraId>.
        source_url (Union[Unset, str]): Credentials are redacted.
        status (Union[Unset, GetWatchResponse200Status]):
        sync_error (Union[None, Unset, str]):
        synced_at (Union[None, Unset, datetime.datetime]):
    """

    agent: Union["GetWatchResponse200AgentType0", None, Unset] = UNSET
    camera: Union["GetWatchResponse200CameraType0", None, Unset] = UNSET
    core_state: Union[Unset, GetWatchResponse200CoreState] = UNSET
    created_at: Union[Unset, datetime.datetime] = UNSET
    display_status: Union[Unset, GetWatchResponse200DisplayStatus] = UNSET
    engine: Union["GetWatchResponse200EngineType0", None, Unset] = UNSET
    event_count: Union[Unset, int] = UNSET
    goal: Union[Unset, str] = UNSET
    id: Union[Unset, str] = UNSET
    last_delivery: Union[GetWatchResponse200LastDeliveryType1, None, Unset] = UNSET
    last_event: Union["GetWatchResponse200LastEventType0", None, Unset] = UNSET
    no_video_since: Union[None, Unset, datetime.datetime] = UNSET
    notify: Union[Unset, "GetWatchResponse200Notify"] = UNSET
    paused_reason: Union[None, Unset, str] = UNSET
    runtime: Union[Unset, GetWatchResponse200Runtime] = UNSET
    secret_hint: Union[None, Unset, str] = UNSET
    site: Union["GetWatchResponse200SiteType0", None, Unset] = UNSET
    source_type: Union[Unset, GetWatchResponse200SourceType] = UNSET
    source_url: Union[Unset, str] = UNSET
    status: Union[Unset, GetWatchResponse200Status] = UNSET
    sync_error: Union[None, Unset, str] = UNSET
    synced_at: Union[None, Unset, datetime.datetime] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.get_watch_response_200_agent_type_0 import (
            GetWatchResponse200AgentType0,
        )
        from ..models.get_watch_response_200_camera_type_0 import (
            GetWatchResponse200CameraType0,
        )
        from ..models.get_watch_response_200_engine_type_0 import (
            GetWatchResponse200EngineType0,
        )
        from ..models.get_watch_response_200_last_event_type_0 import (
            GetWatchResponse200LastEventType0,
        )
        from ..models.get_watch_response_200_site_type_0 import (
            GetWatchResponse200SiteType0,
        )

        agent: Union[None, Unset, dict[str, Any]]
        if isinstance(self.agent, Unset):
            agent = UNSET
        elif isinstance(self.agent, GetWatchResponse200AgentType0):
            agent = self.agent.to_dict()
        else:
            agent = self.agent

        camera: Union[None, Unset, dict[str, Any]]
        if isinstance(self.camera, Unset):
            camera = UNSET
        elif isinstance(self.camera, GetWatchResponse200CameraType0):
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

        engine: Union[None, Unset, dict[str, Any]]
        if isinstance(self.engine, Unset):
            engine = UNSET
        elif isinstance(self.engine, GetWatchResponse200EngineType0):
            engine = self.engine.to_dict()
        else:
            engine = self.engine

        event_count = self.event_count

        goal = self.goal

        id = self.id

        last_delivery: Union[None, Unset, str]
        if isinstance(self.last_delivery, Unset):
            last_delivery = UNSET
        elif isinstance(self.last_delivery, GetWatchResponse200LastDeliveryType1):
            last_delivery = self.last_delivery.value
        else:
            last_delivery = self.last_delivery

        last_event: Union[None, Unset, dict[str, Any]]
        if isinstance(self.last_event, Unset):
            last_event = UNSET
        elif isinstance(self.last_event, GetWatchResponse200LastEventType0):
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

        secret_hint: Union[None, Unset, str]
        if isinstance(self.secret_hint, Unset):
            secret_hint = UNSET
        else:
            secret_hint = self.secret_hint

        site: Union[None, Unset, dict[str, Any]]
        if isinstance(self.site, Unset):
            site = UNSET
        elif isinstance(self.site, GetWatchResponse200SiteType0):
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
        if engine is not UNSET:
            field_dict["engine"] = engine
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
        if secret_hint is not UNSET:
            field_dict["secretHint"] = secret_hint
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
        from ..models.get_watch_response_200_agent_type_0 import (
            GetWatchResponse200AgentType0,
        )
        from ..models.get_watch_response_200_camera_type_0 import (
            GetWatchResponse200CameraType0,
        )
        from ..models.get_watch_response_200_engine_type_0 import (
            GetWatchResponse200EngineType0,
        )
        from ..models.get_watch_response_200_last_event_type_0 import (
            GetWatchResponse200LastEventType0,
        )
        from ..models.get_watch_response_200_notify import GetWatchResponse200Notify
        from ..models.get_watch_response_200_site_type_0 import (
            GetWatchResponse200SiteType0,
        )

        d = dict(src_dict)

        def _parse_agent(
            data: object,
        ) -> Union["GetWatchResponse200AgentType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                agent_type_0 = GetWatchResponse200AgentType0.from_dict(data)

                return agent_type_0
            except:  # noqa: E722
                pass
            return cast(Union["GetWatchResponse200AgentType0", None, Unset], data)

        agent = _parse_agent(d.pop("agent", UNSET))

        def _parse_camera(
            data: object,
        ) -> Union["GetWatchResponse200CameraType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                camera_type_0 = GetWatchResponse200CameraType0.from_dict(data)

                return camera_type_0
            except:  # noqa: E722
                pass
            return cast(Union["GetWatchResponse200CameraType0", None, Unset], data)

        camera = _parse_camera(d.pop("camera", UNSET))

        _core_state = d.pop("coreState", UNSET)
        core_state: Union[Unset, GetWatchResponse200CoreState]
        if isinstance(_core_state, Unset):
            core_state = UNSET
        else:
            core_state = GetWatchResponse200CoreState(_core_state)

        _created_at = d.pop("createdAt", UNSET)
        created_at: Union[Unset, datetime.datetime]
        if isinstance(_created_at, Unset):
            created_at = UNSET
        else:
            created_at = isoparse(_created_at)

        _display_status = d.pop("displayStatus", UNSET)
        display_status: Union[Unset, GetWatchResponse200DisplayStatus]
        if isinstance(_display_status, Unset):
            display_status = UNSET
        else:
            display_status = GetWatchResponse200DisplayStatus(_display_status)

        def _parse_engine(
            data: object,
        ) -> Union["GetWatchResponse200EngineType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                engine_type_0 = GetWatchResponse200EngineType0.from_dict(data)

                return engine_type_0
            except:  # noqa: E722
                pass
            return cast(Union["GetWatchResponse200EngineType0", None, Unset], data)

        engine = _parse_engine(d.pop("engine", UNSET))

        event_count = d.pop("eventCount", UNSET)

        goal = d.pop("goal", UNSET)

        id = d.pop("id", UNSET)

        def _parse_last_delivery(
            data: object,
        ) -> Union[GetWatchResponse200LastDeliveryType1, None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                last_delivery_type_1 = GetWatchResponse200LastDeliveryType1(data)

                return last_delivery_type_1
            except:  # noqa: E722
                pass
            return cast(Union[GetWatchResponse200LastDeliveryType1, None, Unset], data)

        last_delivery = _parse_last_delivery(d.pop("lastDelivery", UNSET))

        def _parse_last_event(
            data: object,
        ) -> Union["GetWatchResponse200LastEventType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                last_event_type_0 = GetWatchResponse200LastEventType0.from_dict(data)

                return last_event_type_0
            except:  # noqa: E722
                pass
            return cast(Union["GetWatchResponse200LastEventType0", None, Unset], data)

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
        notify: Union[Unset, GetWatchResponse200Notify]
        if isinstance(_notify, Unset):
            notify = UNSET
        else:
            notify = GetWatchResponse200Notify.from_dict(_notify)

        def _parse_paused_reason(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        paused_reason = _parse_paused_reason(d.pop("pausedReason", UNSET))

        _runtime = d.pop("runtime", UNSET)
        runtime: Union[Unset, GetWatchResponse200Runtime]
        if isinstance(_runtime, Unset):
            runtime = UNSET
        else:
            runtime = GetWatchResponse200Runtime(_runtime)

        def _parse_secret_hint(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        secret_hint = _parse_secret_hint(d.pop("secretHint", UNSET))

        def _parse_site(
            data: object,
        ) -> Union["GetWatchResponse200SiteType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                site_type_0 = GetWatchResponse200SiteType0.from_dict(data)

                return site_type_0
            except:  # noqa: E722
                pass
            return cast(Union["GetWatchResponse200SiteType0", None, Unset], data)

        site = _parse_site(d.pop("site", UNSET))

        _source_type = d.pop("sourceType", UNSET)
        source_type: Union[Unset, GetWatchResponse200SourceType]
        if isinstance(_source_type, Unset):
            source_type = UNSET
        else:
            source_type = GetWatchResponse200SourceType(_source_type)

        source_url = d.pop("sourceUrl", UNSET)

        _status = d.pop("status", UNSET)
        status: Union[Unset, GetWatchResponse200Status]
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = GetWatchResponse200Status(_status)

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

        get_watch_response_200 = cls(
            agent=agent,
            camera=camera,
            core_state=core_state,
            created_at=created_at,
            display_status=display_status,
            engine=engine,
            event_count=event_count,
            goal=goal,
            id=id,
            last_delivery=last_delivery,
            last_event=last_event,
            no_video_since=no_video_since,
            notify=notify,
            paused_reason=paused_reason,
            runtime=runtime,
            secret_hint=secret_hint,
            site=site,
            source_type=source_type,
            source_url=source_url,
            status=status,
            sync_error=sync_error,
            synced_at=synced_at,
        )

        get_watch_response_200.additional_properties = d
        return get_watch_response_200

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
