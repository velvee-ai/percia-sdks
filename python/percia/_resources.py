"""Small resource namespaces over the generated operations (sync). Return values are the generated attrs models
(see ``percia._generated.models``); request bodies may be the generated body models or plain dicts in the API's JSON
shape (camelCase keys), e.g. ``{"sourceUrl": ..., "goal": ..., "notify": {...}}``.

NOTE: ``_aresources.py`` is the async twin of this file. Keep them in step (tests/test_twins.py checks the method names).
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Callable, Dict, Iterator, List, Mapping, Optional, Union

from ._billing import Billing, billing_of
from ._config import coerce_body, time_param
from ._errors import NotFoundError, PerciaError
from ._generated.api.billing import get_plan as _get_plan
from ._generated.api.billing import get_usage as _get_usage
from ._generated.api.cameras import create_camera as _create_camera
from ._generated.api.cameras import create_camera_pairing as _create_camera_pairing
from ._generated.api.cameras import create_cameras as _create_cameras
from ._generated.api.cameras import delete_camera as _delete_camera
from ._generated.api.cameras import get_camera_status as _get_camera_status
from ._generated.api.cameras import list_cameras as _list_cameras
from ._generated.api.cameras import revoke_camera_token as _revoke_camera_token
from ._generated.api.cameras import rotate_camera_token as _rotate_camera_token
from ._generated.api.events import get_sample_event as _get_sample_event
from ._generated.api.events import list_account_events as _list_account_events
from ._generated.api.hooks import create_hook as _create_hook
from ._generated.api.hooks import delete_hook as _delete_hook
from ._generated.api.hooks import list_hooks as _list_hooks
from ._generated.api.hooks import test_hook as _test_hook
from ._generated.api.identity import get_account as _get_account
from ._generated.api.identity import get_whoami as _get_whoami
from ._generated.api.integrations import create_connect_link as _create_connect_link
from ._generated.api.integrations import delete_integration as _delete_integration
from ._generated.api.integrations import list_integration_services as _list_integration_services
from ._generated.api.integrations import list_integrations as _list_integrations
from ._generated.api.integrations import list_watch_integrations as _list_watch_integrations
from ._generated.api.integrations import set_watch_integrations as _set_watch_integrations
from ._generated.api.watches import create_watch as _create_watch
from ._generated.api.watches import delete_watch as _delete_watch
from ._generated.api.watches import get_watch as _get_watch
from ._generated.api.watches import list_watch_events as _list_watch_events
from ._generated.api.watches import list_watches as _list_watches
from ._generated.api.watches import rotate_watch_secret as _rotate_watch_secret
from ._generated.api.watches import test_watch_delivery as _test_watch_delivery
from ._generated.api.watches import update_watch as _update_watch
from ._generated.models.create_camera_body import CreateCameraBody
from ._generated.models.create_cameras_body import CreateCamerasBody
from ._generated.models.create_connect_link_body import CreateConnectLinkBody
from ._generated.models.create_hook_body import CreateHookBody
from ._generated.models.create_watch_body import CreateWatchBody
from ._generated.models.set_watch_integrations_body import SetWatchIntegrationsBody
from ._generated.models.update_watch_body import UpdateWatchBody
from ._push import (
    BULK_MAX,
    CameraStatus,
    PushRegistration,
    derive_status,
    registration_from_dict,
    status_from_model,
)
from ._stream import StreamItem, stream_events

if TYPE_CHECKING:
    from ._client import Percia

Body = Mapping[str, Any]


def _page_args(limit: Optional[int], cursor: Optional[str]) -> Dict[str, Any]:
    return {k: v for k, v in (("limit", limit), ("cursor", cursor)) if v is not None}


class Watches:
    def __init__(self, client: Percia) -> None:
        self._c = client

    def list(self) -> Any:
        """Your watches (``list[Watch]``)."""
        return self._c._call(_list_watches)

    def get(self, id: str) -> Any:  # noqa: A002
        return self._c._call(_get_watch, id=id)

    def create(self, body: Union[CreateWatchBody, Body]) -> Any:
        """Create a watch. The response holds ``webhook_secret`` (webhook watches) once: save it.

        A clear goal creates the watch; an unclear one answers 422 ``clarification_needed``, and parts that cannot be
        watched answer 409 ``unsupported_not_acknowledged`` (repeat with ``acknowledge_unsupported=True`` after telling the person).
        """
        return self._c._call(_create_watch, body=coerce_body(CreateWatchBody, body))

    def update(self, id: str, body: Union[UpdateWatchBody, Body]) -> Any:  # noqa: A002
        return self._c._call(_update_watch, id=id, body=coerce_body(UpdateWatchBody, body))

    def pause(self, id: str) -> Any:  # noqa: A002
        return self.update(id, {"status": "paused"})

    def resume(self, id: str) -> Any:  # noqa: A002
        return self.update(id, {"status": "active"})

    def delete(self, id: str) -> Any:  # noqa: A002
        return self._c._call(_delete_watch, id=id)

    def test_delivery(self, id: str) -> Any:  # noqa: A002
        """Send a signed test event to the watch's webhook target (no camera needed)."""
        return self._c._call(_test_watch_delivery, id=id)

    def rotate_secret(self, id: str) -> Any:  # noqa: A002
        """Replace the webhook secret immediately; the old one stops verifying at once."""
        return self._c._call(_rotate_watch_secret, id=id)

    def events(self, id: str, *, limit: Optional[int] = None, cursor: Optional[str] = None) -> Any:  # noqa: A002
        """One page of events for a watch (``EventPage``). Use ``client.iter_watch_events`` to walk all pages."""
        return self._c._call(_list_watch_events, id=id, **_page_args(limit, cursor))


class Events:
    def __init__(self, client: Percia) -> None:
        self._c = client

    def list(
        self,
        *,
        limit: Optional[int] = None,
        cursor: Optional[str] = None,
        watch_id: Optional[str] = None,
        type: Optional[str] = None,  # noqa: A002
        since: Union[None, str, int, float, Any] = None,
    ) -> Any:
        """One page of the account-wide event feed, newest first (``EventPage``). Needs ``events:read``."""
        kw = {"watch_id": watch_id, "type_": type, "since": time_param(since), **_page_args(limit, cursor)}
        return self._c._call(_list_account_events, **{k: v for k, v in kw.items() if v is not None})

    def sample(self) -> Any:
        """One example event in the shape of the feed (for connector editors)."""
        return self._c._call(_get_sample_event)

    def stream(
        self,
        *,
        watch_id: Optional[str] = None,
        concern_id: Optional[str] = None,
        type: Optional[str] = None,  # noqa: A002
        backlog: Optional[int] = None,
        since: Union[None, int, str] = None,
        max_reconnects: Optional[int] = None,
        idle_timeout: Optional[float] = 45.0,
        dedupe: bool = True,
        jitter: Optional[Callable[[], float]] = None,
    ) -> Iterator[StreamItem]:
        """Follow the developer event feed (``GET /api/events/stream``, Server-Sent Events) for local development and tests.

        Not a delivery path: webhooks stay the production path. Yields ``Open``, ``Event``, ``Resync``, ``End``,
        ``Reconnect`` and ``Ping`` items and reconnects by itself with the last cursor (``Last-Event-ID``), honouring
        ``Retry-After``. ``Event.data`` is the exact JSON string the server sent (sign and forward that string).
        Raises ``AuthenticationError`` (401), ``InsufficientScopeError`` (403, needs ``events:read``), ``NotFoundError``
        (a watch that is not yours) or ``ValidationError`` (a bad filter) without retrying. ``break`` to stop.
        """
        return stream_events(
            self._c, watch_id=watch_id, concern_id=concern_id, type=type, backlog=backlog, since=since,
            max_reconnects=max_reconnects, idle_timeout=idle_timeout, dedupe=dedupe, jitter=jitter,
        )  # fmt: skip


class Cameras:
    def __init__(self, client: Percia) -> None:
        self._c = client

    def list(self) -> Any:
        return self._c._call(_list_cameras)

    def create(self, name: str, *, device_kind: Optional[str] = None) -> Any:
        """Create a phone camera. The response has ``pair_url``: single use, 10 minutes, a person opens it on the phone.

        ``device_kind`` (``"phone"``, ``"tablet"`` or ``"computer"``) only changes the wording shown to the person.
        """
        body: Dict[str, Any] = {"name": name}
        if device_kind:
            body["deviceKind"] = device_kind
        return self._c._call(_create_camera, body=coerce_body(CreateCameraBody, body))

    def pair(self, id: str) -> Any:  # noqa: A002
        """A fresh pairing link for an existing camera."""
        return self._c._call(_create_camera_pairing, id=id)

    def delete(self, id: str) -> Any:  # noqa: A002
        return self._c._call(_delete_camera, id=id)

    def register_push(self, name: str, external_id: str, *, on_existing: str = "return") -> PushRegistration:
        """Register a camera that a connector on a private network pushes to Percia (WHIP). Safe to call on every start:
        it is idempotent by ``external_id``. The first call returns ``token`` (shown once: store it); later calls return the
        same camera with ``token=None`` and ``existing=True`` unless ``on_existing`` says otherwise: ``"return"`` (default),
        ``"rotate"`` (mint a new token; the old one stops working) or ``"throw"`` (raise ``PerciaError``)."""
        res = self._c._call(
            _create_camera,
            body=coerce_body(CreateCameraBody, {"name": name, "kind": "push", "externalId": external_id}),
        )
        camera = getattr(res, "camera", None)
        whip_url = getattr(res, "whip_url", None)
        if not isinstance(whip_url, str) or camera is None or not getattr(camera, "id", None):
            raise PerciaError(
                'Percia did not return a push camera (no id or whipUrl). Is the server new enough for kind "push"?'
            )
        existing = getattr(res, "existing", False) is True
        token = getattr(res, "token", None)
        token = token if isinstance(token, str) else None
        publish = getattr(res, "publish", None)
        publish = publish.to_dict() if publish is not None and hasattr(publish, "to_dict") else None
        reg = PushRegistration(camera=camera, whip_url=whip_url, token=token, existing=existing, publish=publish)
        reg = self._apply_on_existing(reg, external_id, on_existing)
        return reg

    def rotate_token(self, id: str) -> Any:  # noqa: A002
        """New publish token for a push camera, shown once; the old one stops working at once. A phone camera answers 409
        ``wrong_kind``. Needs ``cameras:write`` and ``watches:delete``."""
        return self._c._call(_rotate_camera_token, id=id)

    def revoke_token(self, id: str) -> Any:  # noqa: A002
        """Stop accepting publishes for a push camera; the camera stays. ``rotate_token`` publishes again."""
        return self._c._call(_revoke_camera_token, id=id)

    def status(self, id: str) -> CameraStatus:  # noqa: A002
        """One camera's state from ``GET /cameras/{id}/status``: ``state`` (``waiting`` | ``online`` | ``offline`` | ``revoked``),
        ``status`` (online = seen in the last 60 s, offline, never), ``last_seen_at``, ``seconds_since_seen``, ``watch_count``
        and a ``hint`` naming the likely reason and the next step. Needs ``cameras:read``.

        An older server without that route answers 404: the SDK then reads ``GET /cameras`` and derives ``state``
        (``derived=True``, ``hint=None``, never ``revoked``). A camera that is not yours raises ``NotFoundError`` either way."""
        try:
            res = self._c._call(_get_camera_status, id=id)
            return status_from_model(res)
        except NotFoundError as err:
            cams = self.list()
            for cam in cams or []:
                if getattr(cam, "id", None) == id:
                    return derive_status(cam)
            raise err

    def bulk(self, items: List[Mapping[str, str]], *, on_existing: str = "return") -> List[Dict[str, Any]]:
        """Register many push cameras (idempotent each) with ``POST /cameras/bulk``: up to 10 per request, so longer lists go
        in chunks of 10. Each chunk is all or nothing against the camera limit (429 ``camera_limit``, nothing created): that
        error is reported on every item of the chunk and later chunks still run. Results keep the input order:
        ``{"external_id", "ok": True, "registration"}`` or ``{"external_id", "ok": False, "error"}``.
        A server without the bulk route answers 404: the SDK then calls ``register_push`` per item. Needs ``cameras:write``;
        ``external_id`` must be unique within a chunk."""
        out: List[Optional[Dict[str, Any]]] = [None] * len(items)
        legacy = False
        for start in range(0, len(items), BULK_MAX):
            idx = list(range(start, min(start + BULK_MAX, len(items))))
            if not legacy:
                try:
                    body = coerce_body(
                        CreateCamerasBody,
                        {"cameras": [{"name": items[i]["name"], "externalId": items[i]["external_id"]} for i in idx]},
                    )
                    res = self._c._call_json(_create_cameras, body=body)
                except NotFoundError:
                    legacy = True
                except PerciaError as exc:
                    for i in idx:
                        out[i] = {"external_id": items[i]["external_id"], "ok": False, "error": exc}
                    continue
                else:
                    entries = [e for e in ((res or {}).get("cameras") or []) if isinstance(e, dict)]
                    for k, i in enumerate(idx):
                        ext = items[i]["external_id"]
                        entry = next((e for e in entries if (e.get("camera") or {}).get("externalId") == ext), None)
                        if entry is None and k < len(entries):
                            entry = entries[k]
                        try:
                            reg = registration_from_dict(entry or {})
                            reg = self._apply_on_existing(reg, ext, on_existing)
                            out[i] = {"external_id": ext, "ok": True, "registration": reg}
                        except PerciaError as exc:
                            out[i] = {"external_id": ext, "ok": False, "error": exc}
                    continue
            for i in idx:
                ext = items[i]["external_id"]
                try:
                    reg = self.register_push(items[i]["name"], ext, on_existing=on_existing)
                    out[i] = {"external_id": ext, "ok": True, "registration": reg}
                except PerciaError as exc:
                    out[i] = {"external_id": ext, "ok": False, "error": exc}
        return [o for o in out if o is not None]

    def _apply_on_existing(self, reg: PushRegistration, external_id: str, mode: str) -> PushRegistration:
        if not reg.existing or reg.token is not None:
            return reg
        if mode == "throw":
            raise PerciaError(
                f'Camera with external_id "{external_id}" already exists ({reg.camera.id}) and its token is shown only once. '
                f'Use cameras.rotate_token("{reg.camera.id}") for a new one.'
            )
        if mode == "rotate":
            rot = self.rotate_token(reg.camera.id)
            new_token = rot.token if isinstance(rot.token, str) else None
            new_url = rot.whip_url if isinstance(rot.whip_url, str) else reg.whip_url
            return PushRegistration(
                camera=reg.camera, whip_url=new_url, token=new_token, existing=True, rotated=True, publish=reg.publish
            )
        return reg


class Integrations:
    def __init__(self, client: Percia) -> None:
        self._c = client

    def services(self) -> Any:
        return self._c._call(_list_integration_services)

    def list(self) -> Any:
        return self._c._call(_list_integrations)

    def connect(self, service: str, **fields: Any) -> Any:
        """Start a connect link for Slack, Discord, Telegram, Home Assistant, IFTTT, Teams, PagerDuty or a webhook.
        The response has ``connect_url``: a person must open it while signed in; you cannot finish it for them."""
        return self._c._call(
            _create_connect_link, body=coerce_body(CreateConnectLinkBody, {"service": service, **fields})
        )

    def delete(self, id: str) -> Any:  # noqa: A002
        return self._c._call(_delete_integration, id=id)

    def watch_rules(self, watch_id: str) -> Any:
        return self._c._call(_list_watch_integrations, id=watch_id)

    def set_watch_rules(self, watch_id: str, rules: Union[SetWatchIntegrationsBody, Body]) -> Any:
        """``rules`` is ``{"rules": [{"connectionId": ..., "on": "*"}]}``."""
        return self._c._call(_set_watch_integrations, id=watch_id, body=coerce_body(SetWatchIntegrationsBody, rules))


class Hooks:
    def __init__(self, client: Percia) -> None:
        self._c = client

    def list(self) -> Any:
        return self._c._call(_list_hooks)

    def create(
        self,
        url: str,
        events: Optional[List[str]] = None,
        *,
        watch_id: Optional[str] = None,
        label: Optional[str] = None,
    ) -> Any:
        """Register a REST hook (needs ``hooks:write``). The response has ``secret`` once: use it to verify deliveries."""
        body: Dict[str, Any] = {"url": url, "events": events or ["goal.met"]}
        if watch_id:
            body["watchId"] = watch_id
        if label:
            body["label"] = label
        return self._c._call(_create_hook, body=coerce_body(CreateHookBody, body))

    def delete(self, id: str) -> Any:  # noqa: A002
        """Idempotent: a hook that is already gone still answers ``deleted: false``."""
        return self._c._call(_delete_hook, id=id)

    def test(self, id: str) -> Any:  # noqa: A002
        """Send one signed ``goal.test`` event now; answers ``{status, ms}``."""
        return self._c._call(_test_hook, id=id)


class Account:
    def __init__(self, client: Percia) -> None:
        self._c = client

    def whoami(self) -> Any:
        """Who the credential belongs to (``GET /api/whoami``): a connection test that any valid API key, OAuth token or
        session passes, whatever its scopes. Returns ``user_id``, ``credential`` (``key``, ``oauth`` or ``session``) and
        ``scopes`` (``None`` for a session); a key adds ``key_name``, an OAuth token ``app_name`` and ``account`` (the
        masked address), a session ``email``. A bad credential raises ``AuthenticationError``."""
        return self._c._call(_get_whoami)

    def get_me(self) -> Any:
        """The user and their subscription (plain JSON: the API documents no schema for it)."""
        return self._c._call(_get_account)

    def plan(self) -> Any:
        """Plan, free and credit minutes, how the account is charged and the next step. Read ``can_start_watches`` first."""
        return self._c._call(_get_plan)

    def usage(self) -> Any:
        """This month's usage."""
        return self._c._call(_get_usage)

    def billing(self) -> Billing:
        """The same facts as the ``billing`` block of MCP ``whoami``, from ``plan()`` (see ``billing_of``)."""
        plan = self.plan()
        return billing_of(plan)
