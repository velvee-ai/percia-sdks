from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.update_watch_body import UpdateWatchBody
from ...models.watch import Watch
from ...types import Response


def _get_kwargs(
    id: str,
    *,
    body: UpdateWatchBody,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": "/watches/{id}".format(
            id=id,
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Error, Watch]]:
    if response.status_code == 200:
        response_200 = Watch.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = Error.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = Error.from_dict(response.json())

        return response_401

    if response.status_code == 402:
        response_402 = Error.from_dict(response.json())

        return response_402

    if response.status_code == 404:
        response_404 = Error.from_dict(response.json())

        return response_404

    if response.status_code == 409:
        response_409 = Error.from_dict(response.json())

        return response_409

    if response.status_code == 422:
        response_422 = Error.from_dict(response.json())

        return response_422

    if response.status_code == 429:
        response_429 = Error.from_dict(response.json())

        return response_429

    if response.status_code == 503:
        response_503 = Error.from_dict(response.json())

        return response_503

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Error, Watch]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: str,
    *,
    client: AuthenticatedClient,
    body: UpdateWatchBody,
) -> Response[Union[Error, Watch]]:
    r"""Update a watch. `status: \"active\"` with `testRun: true` starts a 30-minute live test run (events
    are marked test events); `status: \"active\"` alone goes live, also from a running test, with no
    restart. A new `goal` is read by Percia as on create, before anything changes: a running watch
    judges the new conditions within seconds, a paused one stays paused, and the answer carries
    `understanding`. If the goal cannot be accepted, nothing in the request is applied and the watch
    keeps its earlier goal: 422 `clarification_needed` (`question`, `options`; send the PATCH again with
    the answer in `goal`), 409 `unsupported_not_acknowledged` (leave that part out, or add
    `acknowledgeUnsupported: true`), 422 `draft_refused` or `draft_multi_watch`, 503
    `layer_unavailable`, `layer_unconfigured` or `layer_budget`, 429 `rate_limited`. Earlier events are
    not rewritten. On a watch made with `advanced` conditions the goal only renames it. Deploying or re-
    pinning an agent (`agentId`, `agentVersion`) is not available: 422 `agent_deploy_unavailable`,
    nothing changes.

    Args:
        id (str):
        body (UpdateWatchBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, Watch]]
    """

    kwargs = _get_kwargs(
        id=id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    id: str,
    *,
    client: AuthenticatedClient,
    body: UpdateWatchBody,
) -> Optional[Union[Error, Watch]]:
    r"""Update a watch. `status: \"active\"` with `testRun: true` starts a 30-minute live test run (events
    are marked test events); `status: \"active\"` alone goes live, also from a running test, with no
    restart. A new `goal` is read by Percia as on create, before anything changes: a running watch
    judges the new conditions within seconds, a paused one stays paused, and the answer carries
    `understanding`. If the goal cannot be accepted, nothing in the request is applied and the watch
    keeps its earlier goal: 422 `clarification_needed` (`question`, `options`; send the PATCH again with
    the answer in `goal`), 409 `unsupported_not_acknowledged` (leave that part out, or add
    `acknowledgeUnsupported: true`), 422 `draft_refused` or `draft_multi_watch`, 503
    `layer_unavailable`, `layer_unconfigured` or `layer_budget`, 429 `rate_limited`. Earlier events are
    not rewritten. On a watch made with `advanced` conditions the goal only renames it. Deploying or re-
    pinning an agent (`agentId`, `agentVersion`) is not available: 422 `agent_deploy_unavailable`,
    nothing changes.

    Args:
        id (str):
        body (UpdateWatchBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, Watch]
    """

    return sync_detailed(
        id=id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    id: str,
    *,
    client: AuthenticatedClient,
    body: UpdateWatchBody,
) -> Response[Union[Error, Watch]]:
    r"""Update a watch. `status: \"active\"` with `testRun: true` starts a 30-minute live test run (events
    are marked test events); `status: \"active\"` alone goes live, also from a running test, with no
    restart. A new `goal` is read by Percia as on create, before anything changes: a running watch
    judges the new conditions within seconds, a paused one stays paused, and the answer carries
    `understanding`. If the goal cannot be accepted, nothing in the request is applied and the watch
    keeps its earlier goal: 422 `clarification_needed` (`question`, `options`; send the PATCH again with
    the answer in `goal`), 409 `unsupported_not_acknowledged` (leave that part out, or add
    `acknowledgeUnsupported: true`), 422 `draft_refused` or `draft_multi_watch`, 503
    `layer_unavailable`, `layer_unconfigured` or `layer_budget`, 429 `rate_limited`. Earlier events are
    not rewritten. On a watch made with `advanced` conditions the goal only renames it. Deploying or re-
    pinning an agent (`agentId`, `agentVersion`) is not available: 422 `agent_deploy_unavailable`,
    nothing changes.

    Args:
        id (str):
        body (UpdateWatchBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, Watch]]
    """

    kwargs = _get_kwargs(
        id=id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    id: str,
    *,
    client: AuthenticatedClient,
    body: UpdateWatchBody,
) -> Optional[Union[Error, Watch]]:
    r"""Update a watch. `status: \"active\"` with `testRun: true` starts a 30-minute live test run (events
    are marked test events); `status: \"active\"` alone goes live, also from a running test, with no
    restart. A new `goal` is read by Percia as on create, before anything changes: a running watch
    judges the new conditions within seconds, a paused one stays paused, and the answer carries
    `understanding`. If the goal cannot be accepted, nothing in the request is applied and the watch
    keeps its earlier goal: 422 `clarification_needed` (`question`, `options`; send the PATCH again with
    the answer in `goal`), 409 `unsupported_not_acknowledged` (leave that part out, or add
    `acknowledgeUnsupported: true`), 422 `draft_refused` or `draft_multi_watch`, 503
    `layer_unavailable`, `layer_unconfigured` or `layer_budget`, 429 `rate_limited`. Earlier events are
    not rewritten. On a watch made with `advanced` conditions the goal only renames it. Deploying or re-
    pinning an agent (`agentId`, `agentVersion`) is not available: 422 `agent_deploy_unavailable`,
    nothing changes.

    Args:
        id (str):
        body (UpdateWatchBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, Watch]
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
            body=body,
        )
    ).parsed
