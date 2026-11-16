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

from ..models.create_watch_response_201_core_state import (
    CreateWatchResponse201CoreState,
)
from ..models.create_watch_response_201_display_status import (
    CreateWatchResponse201DisplayStatus,
)
from ..models.create_watch_response_201_last_delivery_type_1 import (
    CreateWatchResponse201LastDeliveryType1,
)
from ..models.create_watch_response_201_runtime import CreateWatchResponse201Runtime
from ..models.create_watch_response_201_source_type import (
    CreateWatchResponse201SourceType,
)
from ..models.create_watch_response_201_status import CreateWatchResponse201Status
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.create_watch_response_201_agent_type_0 import (
        CreateWatchResponse201AgentType0,
    )
    from ..models.create_watch_response_201_camera_type_0 import (
        CreateWatchResponse201CameraType0,
    )
    from ..models.create_watch_response_201_judging import CreateWatchResponse201Judging
    from ..models.create_watch_response_201_last_event_type_0 import (
        CreateWatchResponse201LastEventType0,
    )
    from ..models.create_watch_response_201_notify import CreateWatchResponse201Notify
    from ..models.create_watch_response_201_site_type_0 import (
        CreateWatchResponse201SiteType0,
    )


T = TypeVar("T", bound="CreateWatchResponse201")


@_attrs_define
class CreateWatchResponse201:
    """
    Attributes:
        agent (Union['CreateWatchResponse201AgentType0', None, Unset]): Only on watches deployed with an agent. version
            is the one it runs; followsLatest is true when it was not pinned.
        camera (Union['CreateWatchResponse201CameraType0', None, Unset]): Only on phone-camera watches.
        core_state (Union[Unset, CreateWatchResponse201CoreState]): Only on core watches. running is judging; absent is
            paused (nothing runs on Percia core); off means the core switch was off when it was created; error: see
            syncError.
        created_at (Union[Unset, datetime.datetime]):
        destinations_attached (Union[Unset, int]): Connected destinations that now have a rule on this watch (0 when
            none).
        destinations_failed (Union[Unset, bool]): Only present, true, when destinations could not be read or attached:
            the watch exists without them; add them with PUT /watches/{id}/integrations.
        display_status (Union[Unset, CreateWatchResponse201DisplayStatus]): Needs attention when syncError is set, the
            last delivery failed, a rule of the watch points at a broken integration, or an active watch gets no video
            (noVideoSince set).
        event_count (Union[Unset, int]):
        goal (Union[Unset, str]): For a deployed watch, the agent's name.
        id (Union[Unset, str]):
        judging (Union[Unset, CreateWatchResponse201Judging]): Whether the pool is judging this watch (read-only,
            additive). `state`: judging (a judge call in the last 10 minutes), waiting_for_change (video arrives and the
            picture is still, so nothing is judged; a state goal is still looked at about every 5 minutes), no_video, paused
            (see `reason`), over_budget (the hourly judge limit skipped calls), judge_unavailable, starting, not_running (no
            container reports) or unknown (core runtime). A confirmed no-alert is `judging` or `waiting_for_change` with a
            recent lastFrameAt: silence with state not_running or no_video means nothing was watched. `stalled` is true when
            video flows and a scheduled judge call is 15+ minutes overdue.
        last_delivery (Union[CreateWatchResponse201LastDeliveryType1, None, Unset]): Status of the newest event that is
            not pending. displayStatus comes from this, so a pending event does not hide a failed one.
        last_event (Union['CreateWatchResponse201LastEventType0', None, Unset]):
        no_video_since (Union[None, Unset, datetime.datetime]): When the camera stopped sending video, else null. An
            active watch is paused automatically 60 minutes after this time (pausedReason no_video). Kept on a no_video
            pause; cleared on resume.
        notify (Union[Unset, CreateWatchResponse201Notify]):
        paused_reason (Union[None, Unset, str]): Why a paused watch is paused: user (paused by the owner or an agent, or
            an older pause with no recorded reason), no_video (paused automatically after 60 minutes without video from the
            camera), needs_billing (free minutes and credits used, no card), spend_cap (the monthly cap was reached),
            payment_failed (a payment failed and the 48-hour grace is over; resumes by itself when the payment succeeds) or
            ended (a short-term watch reached its end). Resume with PATCH status active.
        runtime (Union[Unset, CreateWatchResponse201Runtime]): Where the watch is judged: pool (default) or core (Percia
            core, Percept Cloud). Fixed when the watch is created.
        secret_hint (Union[None, Unset, str]):
        site (Union['CreateWatchResponse201SiteType0', None, Unset]): The site this watch belongs to (shared memory),
            else null.
        source_type (Union[Unset, CreateWatchResponse201SourceType]): phone = a paired phone or laptop camera; sourceUrl
            is then percia-cam://<cameraId>.
        source_url (Union[Unset, str]): Credentials are redacted.
        status (Union[Unset, CreateWatchResponse201Status]):
        sync_error (Union[None, Unset, str]):
        synced_at (Union[None, Unset, datetime.datetime]):
        webhook_secret (Union[Unset, str]):
    """

    agent: Union["CreateWatchResponse201AgentType0", None, Unset] = UNSET
    camera: Union["CreateWatchResponse201CameraType0", None, Unset] = UNSET
    core_state: Union[Unset, CreateWatchResponse201CoreState] = UNSET
    created_at: Union[Unset, datetime.datetime] = UNSET
    destinations_attached: Union[Unset, int] = UNSET
    destinations_failed: Union[Unset, bool] = UNSET
    display_status: Union[Unset, CreateWatchResponse201DisplayStatus] = UNSET
    event_count: Union[Unset, int] = UNSET
    goal: Union[Unset, str] = UNSET
    id: Union[Unset, str] = UNSET
    judging: Union[Unset, "CreateWatchResponse201Judging"] = UNSET
    last_delivery: Union[CreateWatchResponse201LastDeliveryType1, None, Unset] = UNSET
    last_event: Union["CreateWatchResponse201LastEventType0", None, Unset] = UNSET
    no_video_since: Union[None, Unset, datetime.datetime] = UNSET
    notify: Union[Unset, "CreateWatchResponse201Notify"] = UNSET
    paused_reason: Union[None, Unset, str] = UNSET
    runtime: Union[Unset, CreateWatchResponse201Runtime] = UNSET
    secret_hint: Union[None, Unset, str] = UNSET
    site: Union["CreateWatchResponse201SiteType0", None, Unset] = UNSET
    source_type: Union[Unset, CreateWatchResponse201SourceType] = UNSET
    source_url: Union[Unset, str] = UNSET
    status: Union[Unset, CreateWatchResponse201Status] = UNSET
    sync_error: Union[None, Unset, str] = UNSET
    synced_at: Union[None, Unset, datetime.datetime] = UNSET
    webhook_secret: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.create_watch_response_201_agent_type_0 import (
            CreateWatchResponse201AgentType0,
        )
        from ..models.create_watch_response_201_camera_type_0 import (
            CreateWatchResponse201CameraType0,
        )
        from ..models.create_watch_response_201_last_event_type_0 import (
            CreateWatchResponse201LastEventType0,
        )
        from ..models.create_watch_response_201_site_type_0 import (
            CreateWatchResponse201SiteType0,
        )

        agent: Union[None, Unset, dict[str, Any]]
        if isinstance(self.agent, Unset):
            agent = UNSET
        elif isinstance(self.agent, CreateWatchResponse201AgentType0):
            agent = self.agent.to_dict()
        else:
            agent = self.agent

        camera: Union[None, Unset, dict[str, Any]]
        if isinstance(self.camera, Unset):
            camera = UNSET
        elif isinstance(self.camera, CreateWatchResponse201CameraType0):
            camera = self.camera.to_dict()
        else:
            camera = self.camera

        core_state: Union[Unset, str] = UNSET
        if not isinstance(self.core_state, Unset):
            core_state = self.core_state.value

        created_at: Union[Unset, str] = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()

        destinations_attached = self.destinations_attached

        destinations_failed = self.destinations_failed

        display_status: Union[Unset, str] = UNSET
        if not isinstance(self.display_status, Unset):
            display_status = self.display_status.value

        event_count = self.event_count

        goal = self.goal

        id = self.id

        judging: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.judging, Unset):
            judging = self.judging.to_dict()

        last_delivery: Union[None, Unset, str]
        if isinstance(self.last_delivery, Unset):
            last_delivery = UNSET
        elif isinstance(self.last_delivery, CreateWatchResponse201LastDeliveryType1):
            last_delivery = self.last_delivery.value
        else:
            last_delivery = self.last_delivery

        last_event: Union[None, Unset, dict[str, Any]]
        if isinstance(self.last_event, Unset):
            last_event = UNSET
        elif isinstance(self.last_event, CreateWatchResponse201LastEventType0):
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
        elif isinstance(self.site, CreateWatchResponse201SiteType0):
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

        webhook_secret = self.webhook_secret

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
        if destinations_attached is not UNSET:
            field_dict["destinationsAttached"] = destinations_attached
        if destinations_failed is not UNSET:
            field_dict["destinationsFailed"] = destinations_failed
        if display_status is not UNSET:
            field_dict["displayStatus"] = display_status
        if event_count is not UNSET:
            field_dict["eventCount"] = event_count
        if goal is not UNSET:
            field_dict["goal"] = goal
        if id is not UNSET:
            field_dict["id"] = id
        if judging is not UNSET:
            field_dict["judging"] = judging
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
        if webhook_secret is not UNSET:
            field_dict["webhookSecret"] = webhook_secret

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.create_watch_response_201_agent_type_0 import (
            CreateWatchResponse201AgentType0,
        )
        from ..models.create_watch_response_201_camera_type_0 import (
            CreateWatchResponse201CameraType0,
        )
        from ..models.create_watch_response_201_judging import (
            CreateWatchResponse201Judging,
        )
        from ..models.create_watch_response_201_last_event_type_0 import (
            CreateWatchResponse201LastEventType0,
        )
        from ..models.create_watch_response_201_notify import (
            CreateWatchResponse201Notify,
        )
        from ..models.create_watch_response_201_site_type_0 import (
            CreateWatchResponse201SiteType0,
        )

        d = dict(src_dict)

        def _parse_agent(
            data: object,
        ) -> Union["CreateWatchResponse201AgentType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                agent_type_0 = CreateWatchResponse201AgentType0.from_dict(data)

                return agent_type_0
            except:  # noqa: E722
                pass
            return cast(Union["CreateWatchResponse201AgentType0", None, Unset], data)

        agent = _parse_agent(d.pop("agent", UNSET))

        def _parse_camera(
            data: object,
        ) -> Union["CreateWatchResponse201CameraType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                camera_type_0 = CreateWatchResponse201CameraType0.from_dict(data)

                return camera_type_0
            except:  # noqa: E722
                pass
            return cast(Union["CreateWatchResponse201CameraType0", None, Unset], data)

        camera = _parse_camera(d.pop("camera", UNSET))

        _core_state = d.pop("coreState", UNSET)
        core_state: Union[Unset, CreateWatchResponse201CoreState]
        if isinstance(_core_state, Unset):
            core_state = UNSET
        else:
            core_state = CreateWatchResponse201CoreState(_core_state)

        _created_at = d.pop("createdAt", UNSET)
        created_at: Union[Unset, datetime.datetime]
        if isinstance(_created_at, Unset):
            created_at = UNSET
        else:
            created_at = isoparse(_created_at)

        destinations_attached = d.pop("destinationsAttached", UNSET)

        destinations_failed = d.pop("destinationsFailed", UNSET)

        _display_status = d.pop("displayStatus", UNSET)
        display_status: Union[Unset, CreateWatchResponse201DisplayStatus]
        if isinstance(_display_status, Unset):
            display_status = UNSET
        else:
            display_status = CreateWatchResponse201DisplayStatus(_display_status)

        event_count = d.pop("eventCount", UNSET)

        goal = d.pop("goal", UNSET)

        id = d.pop("id", UNSET)

        _judging = d.pop("judging", UNSET)
        judging: Union[Unset, CreateWatchResponse201Judging]
        if isinstance(_judging, Unset):
            judging = UNSET
        else:
            judging = CreateWatchResponse201Judging.from_dict(_judging)

        def _parse_last_delivery(
            data: object,
        ) -> Union[CreateWatchResponse201LastDeliveryType1, None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                last_delivery_type_1 = CreateWatchResponse201LastDeliveryType1(data)

                return last_delivery_type_1
            except:  # noqa: E722
                pass
            return cast(Union[CreateWatchResponse201LastDeliveryType1, None, Unset], data)

        last_delivery = _parse_last_delivery(d.pop("lastDelivery", UNSET))

        def _parse_last_event(
            data: object,
        ) -> Union["CreateWatchResponse201LastEventType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                last_event_type_0 = CreateWatchResponse201LastEventType0.from_dict(data)

                return last_event_type_0
            except:  # noqa: E722
                pass
            return cast(Union["CreateWatchResponse201LastEventType0", None, Unset], data)

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
        notify: Union[Unset, CreateWatchResponse201Notify]
        if isinstance(_notify, Unset):
            notify = UNSET
        else:
            notify = CreateWatchResponse201Notify.from_dict(_notify)

        def _parse_paused_reason(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        paused_reason = _parse_paused_reason(d.pop("pausedReason", UNSET))

        _runtime = d.pop("runtime", UNSET)
        runtime: Union[Unset, CreateWatchResponse201Runtime]
        if isinstance(_runtime, Unset):
            runtime = UNSET
        else:
            runtime = CreateWatchResponse201Runtime(_runtime)

        def _parse_secret_hint(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        secret_hint = _parse_secret_hint(d.pop("secretHint", UNSET))

        def _parse_site(
            data: object,
        ) -> Union["CreateWatchResponse201SiteType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                site_type_0 = CreateWatchResponse201SiteType0.from_dict(data)

                return site_type_0
            except:  # noqa: E722
                pass
            return cast(Union["CreateWatchResponse201SiteType0", None, Unset], data)

        site = _parse_site(d.pop("site", UNSET))

        _source_type = d.pop("sourceType", UNSET)
        source_type: Union[Unset, CreateWatchResponse201SourceType]
        if isinstance(_source_type, Unset):
            source_type = UNSET
        else:
            source_type = CreateWatchResponse201SourceType(_source_type)

        source_url = d.pop("sourceUrl", UNSET)

        _status = d.pop("status", UNSET)
        status: Union[Unset, CreateWatchResponse201Status]
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = CreateWatchResponse201Status(_status)

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

        webhook_secret = d.pop("webhookSecret", UNSET)

        create_watch_response_201 = cls(
            agent=agent,
            camera=camera,
            core_state=core_state,
            created_at=created_at,
            destinations_attached=destinations_attached,
            destinations_failed=destinations_failed,
            display_status=display_status,
            event_count=event_count,
            goal=goal,
            id=id,
            judging=judging,
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
            webhook_secret=webhook_secret,
        )

        create_watch_response_201.additional_properties = d
        return create_watch_response_201

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
