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
        created_at (Union[Unset, datetime.datetime]):
        display_status (Union[Unset, CreateWatchResponse201DisplayStatus]): Needs attention when syncError is set, the
            last delivery failed, a rule of the watch points at a broken integration, or an active watch gets no video
            (noVideoSince set).
        event_count (Union[Unset, int]):
        goal (Union[Unset, str]): For a deployed watch, the agent's name.
        id (Union[Unset, str]):
        last_delivery (Union[CreateWatchResponse201LastDeliveryType1, None, Unset]): Status of the newest event that is
            not pending. displayStatus comes from this, so a pending event does not hide a failed one.
        last_event (Union['CreateWatchResponse201LastEventType0', None, Unset]):
        no_video_since (Union[None, Unset, datetime.datetime]): When the camera stopped sending video, else null. An
            active watch is paused automatically 60 minutes after this time (pausedReason no_video). Kept on a no_video
            pause; cleared on resume.
        notify (Union[Unset, CreateWatchResponse201Notify]):
        paused_reason (Union[None, Unset, str]): Why a paused watch is paused: user (paused by the owner or an agent) or
            no_video (paused automatically after 60 minutes without video from the camera). Resume with PATCH status active.
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
    created_at: Union[Unset, datetime.datetime] = UNSET
    display_status: Union[Unset, CreateWatchResponse201DisplayStatus] = UNSET
    event_count: Union[Unset, int] = UNSET
    goal: Union[Unset, str] = UNSET
    id: Union[Unset, str] = UNSET
    last_delivery: Union[CreateWatchResponse201LastDeliveryType1, None, Unset] = UNSET
    last_event: Union["CreateWatchResponse201LastEventType0", None, Unset] = UNSET
    no_video_since: Union[None, Unset, datetime.datetime] = UNSET
    notify: Union[Unset, "CreateWatchResponse201Notify"] = UNSET
    paused_reason: Union[None, Unset, str] = UNSET
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

        _created_at = d.pop("createdAt", UNSET)
        created_at: Union[Unset, datetime.datetime]
        if isinstance(_created_at, Unset):
            created_at = UNSET
        else:
            created_at = isoparse(_created_at)

        _display_status = d.pop("displayStatus", UNSET)
        display_status: Union[Unset, CreateWatchResponse201DisplayStatus]
        if isinstance(_display_status, Unset):
            display_status = UNSET
        else:
            display_status = CreateWatchResponse201DisplayStatus(_display_status)

        event_count = d.pop("eventCount", UNSET)

        goal = d.pop("goal", UNSET)

        id = d.pop("id", UNSET)

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
