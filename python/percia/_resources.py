"""Small resource namespaces over the generated operations (sync). Return values are the generated attrs models
(see ``percia._generated.models``); request bodies may be the generated body models or plain dicts in the API's JSON
shape (camelCase keys), e.g. ``{"sourceUrl": ..., "goal": ..., "notify": {...}}``.

NOTE: ``_aresources.py`` is the async twin of this file. Keep them in step (tests/test_twins.py checks the method names).
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, List, Mapping, Optional, Union

from ._config import coerce_body, time_param
from ._generated.api.cameras import create_camera as _create_camera
from ._generated.api.cameras import create_camera_pairing as _create_camera_pairing
from ._generated.api.cameras import delete_camera as _delete_camera
from ._generated.api.cameras import list_cameras as _list_cameras
from ._generated.api.events import get_sample_event as _get_sample_event
from ._generated.api.events import list_account_events as _list_account_events
from ._generated.api.hooks import create_hook as _create_hook
from ._generated.api.hooks import delete_hook as _delete_hook
from ._generated.api.hooks import list_hooks as _list_hooks
from ._generated.api.hooks import test_hook as _test_hook
from ._generated.api.identity import get_account as _get_account
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
from ._generated.models.create_connect_link_body import CreateConnectLinkBody
from ._generated.models.create_hook_body import CreateHookBody
from ._generated.models.create_watch_body import CreateWatchBody
from ._generated.models.set_watch_integrations_body import SetWatchIntegrationsBody
from ._generated.models.update_watch_body import UpdateWatchBody

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
        """Create a watch. The response holds ``webhook_secret`` (webhook watches) once: save it."""
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


class Cameras:
    def __init__(self, client: Percia) -> None:
        self._c = client

    def list(self) -> Any:
        return self._c._call(_list_cameras)

    def create(self, name: str) -> Any:
        """Create a phone camera. The response has ``pair_url``: single use, 10 minutes, a person opens it on the phone."""
        return self._c._call(_create_camera, body=coerce_body(CreateCameraBody, {"name": name}))

    def pair(self, id: str) -> Any:  # noqa: A002
        """A fresh pairing link for an existing camera."""
        return self._c._call(_create_camera_pairing, id=id)

    def delete(self, id: str) -> Any:  # noqa: A002
        return self._c._call(_delete_camera, id=id)


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

    def get_me(self) -> Any:
        """The user and their subscription (plain JSON: the API documents no schema for it)."""
        return self._c._call(_get_account)
