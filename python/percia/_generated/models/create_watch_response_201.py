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
    from ..models.create_watch_response_201_advanced import (
        CreateWatchResponse201Advanced,
    )
    from ..models.create_watch_response_201_agent_type_0 import (
        CreateWatchResponse201AgentType0,
    )
    from ..models.create_watch_response_201_camera_type_0 import (
        CreateWatchResponse201CameraType0,
    )
    from ..models.create_watch_response_201_destinations_item import (
        CreateWatchResponse201DestinationsItem,
    )
    from ..models.create_watch_response_201_judging import CreateWatchResponse201Judging
    from ..models.create_watch_response_201_last_event_type_0 import (
        CreateWatchResponse201LastEventType0,
    )
    from ..models.create_watch_response_201_notify import CreateWatchResponse201Notify
    from ..models.create_watch_response_201_pending_question_type_0 import (
        CreateWatchResponse201PendingQuestionType0,
    )
    from ..models.create_watch_response_201_site_type_0 import (
        CreateWatchResponse201SiteType0,
    )


T = TypeVar("T", bound="CreateWatchResponse201")


@_attrs_define
class CreateWatchResponse201:
    """
    Attributes:
        advanced (Union[Unset, CreateWatchResponse201Advanced]): Only on a watch made with `advanced` (Percia engine).
            `conditions` and `actions` as you sent them; `contextRequests` are what the engine asked you to supply (each has
            `how_to_supply`, a SiteContext path to PUT), `[]` when none or not yet known; `state` is `pending` until the
            engine reported them; `siteRev` is the revision of the site's context it runs on.
        agent (Union['CreateWatchResponse201AgentType0', None, Unset]): Only on watches deployed with an agent. version
            is the one it runs; followsLatest is true when it was not pinned.
        camera (Union['CreateWatchResponse201CameraType0', None, Unset]): Only on phone-camera watches.
        created_at (Union[Unset, datetime.datetime]):
        delivery_problem (Union[None, Unset, str]): One plain sentence for a watch whose newest settled delivery failed
            ("Slack answered 500."), else null.
        destinations (Union[Unset, list['CreateWatchResponse201DestinationsItem']]): Connected destinations (Slack,
            Discord ...) this watch alerts, from its integration rules. Empty while integrations are off.
        destinations_attached (Union[Unset, int]): Connected destinations that now have a rule on this watch (0 when
            none).
        destinations_failed (Union[Unset, bool]): Only present, true, when destinations could not be read or attached:
            the watch exists without them; add them with PUT /watches/{id}/integrations.
        display_status (Union[Unset, CreateWatchResponse201DisplayStatus]): Needs attention when syncError is set, the
            last delivery failed, a rule of the watch points at a broken integration, or an active watch gets no video
            (noVideoSince set).
        event_count (Union[Unset, int]):
        events24h (Union[Unset, int]): Events in the last 24 hours.
        goal (Union[Unset, str]): For a deployed watch, the agent's name.
        id (Union[Unset, str]):
        judging (Union[Unset, CreateWatchResponse201Judging]): Whether the pool is judging this watch (read-only,
            additive). `state`: judging (a judge call in the last 10 minutes), waiting_for_change (video arrives and the
            picture is still, so nothing is judged; a state goal is still looked at about every 5 minutes), no_video, paused
            (see `reason`), over_budget (the hourly judge limit skipped calls), judge_unavailable, starting (also: no frames
            yet, for up to 4 minutes after the pool started the watch; noVideoSince reads null then), not_running (no
            container reports) or unknown (core runtime). A confirmed no-alert is `judging` or `waiting_for_change` with a
            recent lastFrameAt: silence with state not_running or no_video means nothing was watched. `stalled` is true when
            video flows and a scheduled judge call is 15+ minutes overdue.
        last_delivery (Union[CreateWatchResponse201LastDeliveryType1, None, Unset]): Status of the newest event that is
            not pending. displayStatus comes from this, so a pending event does not hide a failed one.
        last_event (Union['CreateWatchResponse201LastEventType0', None, Unset]):
        minutes_this_month (Union[Unset, int]): Camera-minutes this UTC month on the stream this watch uses (watches on
            one camera share its minutes).
        no_video_since (Union[None, Unset, datetime.datetime]): When the camera stopped sending video, else null. An
            active watch is paused automatically 60 minutes after this time (pausedReason no_video). Kept on a no_video
            pause; cleared on resume.
        notify (Union[Unset, CreateWatchResponse201Notify]):
        paused_reason (Union[None, Unset, str]): Why a paused watch is paused: user (paused by the owner or an agent, or
            an older pause with no recorded reason), no_video (paused automatically after 60 minutes without video from the
            camera), needs_billing (free minutes and credits used, no card), spend_cap (the monthly cap was reached),
            payment_failed (a payment failed and the 48-hour grace is over; resumes by itself when the payment succeeds)
            ended (a short-term watch reached its end) testing (made with `startPaused` to be tested before going live;
            PATCH status active goes live) or test_ended (a 30-minute test run ended; PATCH status active goes live). Resume
            with PATCH status active.
        pending_question (Union['CreateWatchResponse201PendingQuestionType0', None, Unset]): Detail only. A converted
            watch that waits for an answer: the question, its options (may be empty), when it was asked and the draft to
            answer through POST /watches/draft/{draftId}/answer. Null otherwise.
        runtime (Union[Unset, CreateWatchResponse201Runtime]): Always pool (kept for older clients): every watch is
            judged on the Percia engine.
        secret_hint (Union[None, Unset, str]):
        site (Union['CreateWatchResponse201SiteType0', None, Unset]): The site this watch belongs to (shared memory),
            else null.
        source_type (Union[Unset, CreateWatchResponse201SourceType]): phone = a paired phone, tablet or computer camera;
            sourceUrl is then percia-cam://<cameraId>.
        source_url (Union[Unset, str]): Credentials are redacted. A video file is percia-file://<uploadId>.
        status (Union[Unset, CreateWatchResponse201Status]):
        sync_error (Union[None, Unset, str]):
        synced_at (Union[None, Unset, datetime.datetime]):
        test_until (Union[None, Unset, datetime.datetime]): Set while the watch is in a live test run: when it ends (30
            minutes after PATCH {status: "active", testRun: true}). Its events are marked `test: true`, its webhooks carry
            `test: true`, and the watch is paused by itself at this time (pausedReason test_ended). PATCH {status: "active"}
            goes live with no restart; null otherwise.
        webhook_secret (Union[Unset, str]):
    """

    advanced: Union[Unset, "CreateWatchResponse201Advanced"] = UNSET
    agent: Union["CreateWatchResponse201AgentType0", None, Unset] = UNSET
    camera: Union["CreateWatchResponse201CameraType0", None, Unset] = UNSET
    created_at: Union[Unset, datetime.datetime] = UNSET
    delivery_problem: Union[None, Unset, str] = UNSET
    destinations: Union[Unset, list["CreateWatchResponse201DestinationsItem"]] = UNSET
    destinations_attached: Union[Unset, int] = UNSET
    destinations_failed: Union[Unset, bool] = UNSET
    display_status: Union[Unset, CreateWatchResponse201DisplayStatus] = UNSET
    event_count: Union[Unset, int] = UNSET
    events24h: Union[Unset, int] = UNSET
    goal: Union[Unset, str] = UNSET
    id: Union[Unset, str] = UNSET
    judging: Union[Unset, "CreateWatchResponse201Judging"] = UNSET
    last_delivery: Union[CreateWatchResponse201LastDeliveryType1, None, Unset] = UNSET
    last_event: Union["CreateWatchResponse201LastEventType0", None, Unset] = UNSET
    minutes_this_month: Union[Unset, int] = UNSET
    no_video_since: Union[None, Unset, datetime.datetime] = UNSET
    notify: Union[Unset, "CreateWatchResponse201Notify"] = UNSET
    paused_reason: Union[None, Unset, str] = UNSET
    pending_question: Union["CreateWatchResponse201PendingQuestionType0", None, Unset] = UNSET
    runtime: Union[Unset, CreateWatchResponse201Runtime] = UNSET
    secret_hint: Union[None, Unset, str] = UNSET
    site: Union["CreateWatchResponse201SiteType0", None, Unset] = UNSET
    source_type: Union[Unset, CreateWatchResponse201SourceType] = UNSET
    source_url: Union[Unset, str] = UNSET
    status: Union[Unset, CreateWatchResponse201Status] = UNSET
    sync_error: Union[None, Unset, str] = UNSET
    synced_at: Union[None, Unset, datetime.datetime] = UNSET
    test_until: Union[None, Unset, datetime.datetime] = UNSET
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
        from ..models.create_watch_response_201_pending_question_type_0 import (
            CreateWatchResponse201PendingQuestionType0,
        )
        from ..models.create_watch_response_201_site_type_0 import (
            CreateWatchResponse201SiteType0,
        )

        advanced: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.advanced, Unset):
            advanced = self.advanced.to_dict()

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

        created_at: Union[Unset, str] = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()

        delivery_problem: Union[None, Unset, str]
        if isinstance(self.delivery_problem, Unset):
            delivery_problem = UNSET
        else:
            delivery_problem = self.delivery_problem

        destinations: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.destinations, Unset):
            destinations = []
            for destinations_item_data in self.destinations:
                destinations_item = destinations_item_data.to_dict()
                destinations.append(destinations_item)

        destinations_attached = self.destinations_attached

        destinations_failed = self.destinations_failed

        display_status: Union[Unset, str] = UNSET
        if not isinstance(self.display_status, Unset):
            display_status = self.display_status.value

        event_count = self.event_count

        events24h = self.events24h

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

        minutes_this_month = self.minutes_this_month

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

        pending_question: Union[None, Unset, dict[str, Any]]
        if isinstance(self.pending_question, Unset):
            pending_question = UNSET
        elif isinstance(self.pending_question, CreateWatchResponse201PendingQuestionType0):
            pending_question = self.pending_question.to_dict()
        else:
            pending_question = self.pending_question

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

        test_until: Union[None, Unset, str]
        if isinstance(self.test_until, Unset):
            test_until = UNSET
        elif isinstance(self.test_until, datetime.datetime):
            test_until = self.test_until.isoformat()
        else:
            test_until = self.test_until

        webhook_secret = self.webhook_secret

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if advanced is not UNSET:
            field_dict["advanced"] = advanced
        if agent is not UNSET:
            field_dict["agent"] = agent
        if camera is not UNSET:
            field_dict["camera"] = camera
        if created_at is not UNSET:
            field_dict["createdAt"] = created_at
        if delivery_problem is not UNSET:
            field_dict["deliveryProblem"] = delivery_problem
        if destinations is not UNSET:
            field_dict["destinations"] = destinations
        if destinations_attached is not UNSET:
            field_dict["destinationsAttached"] = destinations_attached
        if destinations_failed is not UNSET:
            field_dict["destinationsFailed"] = destinations_failed
        if display_status is not UNSET:
            field_dict["displayStatus"] = display_status
        if event_count is not UNSET:
            field_dict["eventCount"] = event_count
        if events24h is not UNSET:
            field_dict["events24h"] = events24h
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
        if minutes_this_month is not UNSET:
            field_dict["minutesThisMonth"] = minutes_this_month
        if no_video_since is not UNSET:
            field_dict["noVideoSince"] = no_video_since
        if notify is not UNSET:
            field_dict["notify"] = notify
        if paused_reason is not UNSET:
            field_dict["pausedReason"] = paused_reason
        if pending_question is not UNSET:
            field_dict["pendingQuestion"] = pending_question
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
        if test_until is not UNSET:
            field_dict["testUntil"] = test_until
        if webhook_secret is not UNSET:
            field_dict["webhookSecret"] = webhook_secret

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.create_watch_response_201_advanced import (
            CreateWatchResponse201Advanced,
        )
        from ..models.create_watch_response_201_agent_type_0 import (
            CreateWatchResponse201AgentType0,
        )
        from ..models.create_watch_response_201_camera_type_0 import (
            CreateWatchResponse201CameraType0,
        )
        from ..models.create_watch_response_201_destinations_item import (
            CreateWatchResponse201DestinationsItem,
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
        from ..models.create_watch_response_201_pending_question_type_0 import (
            CreateWatchResponse201PendingQuestionType0,
        )
        from ..models.create_watch_response_201_site_type_0 import (
            CreateWatchResponse201SiteType0,
        )

        d = dict(src_dict)
        _advanced = d.pop("advanced", UNSET)
        advanced: Union[Unset, CreateWatchResponse201Advanced]
        if isinstance(_advanced, Unset):
            advanced = UNSET
        else:
            advanced = CreateWatchResponse201Advanced.from_dict(_advanced)

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

        _created_at = d.pop("createdAt", UNSET)
        created_at: Union[Unset, datetime.datetime]
        if isinstance(_created_at, Unset):
            created_at = UNSET
        else:
            created_at = isoparse(_created_at)

        def _parse_delivery_problem(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        delivery_problem = _parse_delivery_problem(d.pop("deliveryProblem", UNSET))

        destinations = []
        _destinations = d.pop("destinations", UNSET)
        for destinations_item_data in _destinations or []:
            destinations_item = CreateWatchResponse201DestinationsItem.from_dict(destinations_item_data)

            destinations.append(destinations_item)

        destinations_attached = d.pop("destinationsAttached", UNSET)

        destinations_failed = d.pop("destinationsFailed", UNSET)

        _display_status = d.pop("displayStatus", UNSET)
        display_status: Union[Unset, CreateWatchResponse201DisplayStatus]
        if isinstance(_display_status, Unset):
            display_status = UNSET
        else:
            display_status = CreateWatchResponse201DisplayStatus(_display_status)

        event_count = d.pop("eventCount", UNSET)

        events24h = d.pop("events24h", UNSET)

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

        minutes_this_month = d.pop("minutesThisMonth", UNSET)

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

        def _parse_pending_question(
            data: object,
        ) -> Union["CreateWatchResponse201PendingQuestionType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                pending_question_type_0 = CreateWatchResponse201PendingQuestionType0.from_dict(data)

                return pending_question_type_0
            except:  # noqa: E722
                pass
            return cast(Union["CreateWatchResponse201PendingQuestionType0", None, Unset], data)

        pending_question = _parse_pending_question(d.pop("pendingQuestion", UNSET))

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

        def _parse_test_until(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                test_until_type_0 = isoparse(data)

                return test_until_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        test_until = _parse_test_until(d.pop("testUntil", UNSET))

        webhook_secret = d.pop("webhookSecret", UNSET)

        create_watch_response_201 = cls(
            advanced=advanced,
            agent=agent,
            camera=camera,
            created_at=created_at,
            delivery_problem=delivery_problem,
            destinations=destinations,
            destinations_attached=destinations_attached,
            destinations_failed=destinations_failed,
            display_status=display_status,
            event_count=event_count,
            events24h=events24h,
            goal=goal,
            id=id,
            judging=judging,
            last_delivery=last_delivery,
            last_event=last_event,
            minutes_this_month=minutes_this_month,
            no_video_since=no_video_since,
            notify=notify,
            paused_reason=paused_reason,
            pending_question=pending_question,
            runtime=runtime,
            secret_hint=secret_hint,
            site=site,
            source_type=source_type,
            source_url=source_url,
            status=status,
            sync_error=sync_error,
            synced_at=synced_at,
            test_until=test_until,
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
