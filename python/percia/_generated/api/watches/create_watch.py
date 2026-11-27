from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_watch_body import CreateWatchBody
from ...models.create_watch_response_201 import CreateWatchResponse201
from ...models.create_watch_response_422 import CreateWatchResponse422
from ...models.error import Error
from ...types import Response


def _get_kwargs(
    *,
    body: CreateWatchBody,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/watches/owned",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[CreateWatchResponse201, CreateWatchResponse422, Error]]:
    if response.status_code == 201:
        response_201 = CreateWatchResponse201.from_dict(response.json())

        return response_201

    if response.status_code == 400:
        response_400 = Error.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = Error.from_dict(response.json())

        return response_401

    if response.status_code == 402:
        response_402 = Error.from_dict(response.json())

        return response_402

    if response.status_code == 409:
        response_409 = Error.from_dict(response.json())

        return response_409

    if response.status_code == 422:
        response_422 = CreateWatchResponse422.from_dict(response.json())

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
) -> Response[Union[CreateWatchResponse201, CreateWatchResponse422, Error]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: CreateWatchBody,
) -> Response[Union[CreateWatchResponse201, CreateWatchResponse422, Error]]:
    r"""Create a watch as the signed-in user (email or webhook; no Turnstile). sourceUrl may be percia-
    cam://<cameraId> for one of your own phone or bridge cameras; a private address (192.168.x.x, an
    NVR) is refused: the person installs the Percia bridge (https://github.com/velvee-ai/percia-bridge)
    to push that camera. Send `goal`, or `agentId` (+ optional `agentVersion`; omitted = follow the
    latest) to deploy a published agent. Optional `runtime: \"core\"` runs it on Percia core (Percept
    Cloud) instead of the default pool: only when Percia has turned core on (otherwise 403), and not for
    phone cameras, agents or sites (400). Leave it out unless the person asked. Percia understands the
    goal by itself (see `interpretation` in the answer; POST /watches/interpret previews it): read
    `interpretation.gaps` and `untestable` and ask the person those questions. Send `draftId` (a ready
    draft from POST /watches/draft, with `acknowledgeUnsupported: true` when it left parts out) instead
    of `goal`; the draft has the conditions. Send `interpret: false` to keep the words exactly as
    written (optionally with `kind`: state or event), or `concerns: [{text, kind, ignore?}]` (1 to 10)
    to give the conditions yourself; not with an agent. With clarifying (when Percia has it on; see GET
    /config): a create with a `goal` is read by Percia's layer first. A clear goal creates the watch as
    before. An unclear one creates nothing and answers 422 `clarification_needed` with `draftId`,
    `question` and `options` (and `guidance`): ask the person, answer with POST
    /watches/draft/{draftId}/answer {text}, then create with {sourceUrl, draftId}; or send a clearer
    goal. Parts that cannot be watched answer 409 `unsupported_not_acknowledged` (tell the person, then
    repeat with `acknowledgeUnsupported: true`). The old per-watch knobs are refused with 422 naming the
    field in `error.field`, from the first call: cooldownS, kind, rearmS, recheckS, minConfidence,
    notWhen, zones, concerns, judgeKey, interpret, and runtime: core.

    Args:
        body (CreateWatchBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CreateWatchResponse201, CreateWatchResponse422, Error]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    body: CreateWatchBody,
) -> Optional[Union[CreateWatchResponse201, CreateWatchResponse422, Error]]:
    r"""Create a watch as the signed-in user (email or webhook; no Turnstile). sourceUrl may be percia-
    cam://<cameraId> for one of your own phone or bridge cameras; a private address (192.168.x.x, an
    NVR) is refused: the person installs the Percia bridge (https://github.com/velvee-ai/percia-bridge)
    to push that camera. Send `goal`, or `agentId` (+ optional `agentVersion`; omitted = follow the
    latest) to deploy a published agent. Optional `runtime: \"core\"` runs it on Percia core (Percept
    Cloud) instead of the default pool: only when Percia has turned core on (otherwise 403), and not for
    phone cameras, agents or sites (400). Leave it out unless the person asked. Percia understands the
    goal by itself (see `interpretation` in the answer; POST /watches/interpret previews it): read
    `interpretation.gaps` and `untestable` and ask the person those questions. Send `draftId` (a ready
    draft from POST /watches/draft, with `acknowledgeUnsupported: true` when it left parts out) instead
    of `goal`; the draft has the conditions. Send `interpret: false` to keep the words exactly as
    written (optionally with `kind`: state or event), or `concerns: [{text, kind, ignore?}]` (1 to 10)
    to give the conditions yourself; not with an agent. With clarifying (when Percia has it on; see GET
    /config): a create with a `goal` is read by Percia's layer first. A clear goal creates the watch as
    before. An unclear one creates nothing and answers 422 `clarification_needed` with `draftId`,
    `question` and `options` (and `guidance`): ask the person, answer with POST
    /watches/draft/{draftId}/answer {text}, then create with {sourceUrl, draftId}; or send a clearer
    goal. Parts that cannot be watched answer 409 `unsupported_not_acknowledged` (tell the person, then
    repeat with `acknowledgeUnsupported: true`). The old per-watch knobs are refused with 422 naming the
    field in `error.field`, from the first call: cooldownS, kind, rearmS, recheckS, minConfidence,
    notWhen, zones, concerns, judgeKey, interpret, and runtime: core.

    Args:
        body (CreateWatchBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CreateWatchResponse201, CreateWatchResponse422, Error]
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: CreateWatchBody,
) -> Response[Union[CreateWatchResponse201, CreateWatchResponse422, Error]]:
    r"""Create a watch as the signed-in user (email or webhook; no Turnstile). sourceUrl may be percia-
    cam://<cameraId> for one of your own phone or bridge cameras; a private address (192.168.x.x, an
    NVR) is refused: the person installs the Percia bridge (https://github.com/velvee-ai/percia-bridge)
    to push that camera. Send `goal`, or `agentId` (+ optional `agentVersion`; omitted = follow the
    latest) to deploy a published agent. Optional `runtime: \"core\"` runs it on Percia core (Percept
    Cloud) instead of the default pool: only when Percia has turned core on (otherwise 403), and not for
    phone cameras, agents or sites (400). Leave it out unless the person asked. Percia understands the
    goal by itself (see `interpretation` in the answer; POST /watches/interpret previews it): read
    `interpretation.gaps` and `untestable` and ask the person those questions. Send `draftId` (a ready
    draft from POST /watches/draft, with `acknowledgeUnsupported: true` when it left parts out) instead
    of `goal`; the draft has the conditions. Send `interpret: false` to keep the words exactly as
    written (optionally with `kind`: state or event), or `concerns: [{text, kind, ignore?}]` (1 to 10)
    to give the conditions yourself; not with an agent. With clarifying (when Percia has it on; see GET
    /config): a create with a `goal` is read by Percia's layer first. A clear goal creates the watch as
    before. An unclear one creates nothing and answers 422 `clarification_needed` with `draftId`,
    `question` and `options` (and `guidance`): ask the person, answer with POST
    /watches/draft/{draftId}/answer {text}, then create with {sourceUrl, draftId}; or send a clearer
    goal. Parts that cannot be watched answer 409 `unsupported_not_acknowledged` (tell the person, then
    repeat with `acknowledgeUnsupported: true`). The old per-watch knobs are refused with 422 naming the
    field in `error.field`, from the first call: cooldownS, kind, rearmS, recheckS, minConfidence,
    notWhen, zones, concerns, judgeKey, interpret, and runtime: core.

    Args:
        body (CreateWatchBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CreateWatchResponse201, CreateWatchResponse422, Error]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: CreateWatchBody,
) -> Optional[Union[CreateWatchResponse201, CreateWatchResponse422, Error]]:
    r"""Create a watch as the signed-in user (email or webhook; no Turnstile). sourceUrl may be percia-
    cam://<cameraId> for one of your own phone or bridge cameras; a private address (192.168.x.x, an
    NVR) is refused: the person installs the Percia bridge (https://github.com/velvee-ai/percia-bridge)
    to push that camera. Send `goal`, or `agentId` (+ optional `agentVersion`; omitted = follow the
    latest) to deploy a published agent. Optional `runtime: \"core\"` runs it on Percia core (Percept
    Cloud) instead of the default pool: only when Percia has turned core on (otherwise 403), and not for
    phone cameras, agents or sites (400). Leave it out unless the person asked. Percia understands the
    goal by itself (see `interpretation` in the answer; POST /watches/interpret previews it): read
    `interpretation.gaps` and `untestable` and ask the person those questions. Send `draftId` (a ready
    draft from POST /watches/draft, with `acknowledgeUnsupported: true` when it left parts out) instead
    of `goal`; the draft has the conditions. Send `interpret: false` to keep the words exactly as
    written (optionally with `kind`: state or event), or `concerns: [{text, kind, ignore?}]` (1 to 10)
    to give the conditions yourself; not with an agent. With clarifying (when Percia has it on; see GET
    /config): a create with a `goal` is read by Percia's layer first. A clear goal creates the watch as
    before. An unclear one creates nothing and answers 422 `clarification_needed` with `draftId`,
    `question` and `options` (and `guidance`): ask the person, answer with POST
    /watches/draft/{draftId}/answer {text}, then create with {sourceUrl, draftId}; or send a clearer
    goal. Parts that cannot be watched answer 409 `unsupported_not_acknowledged` (tell the person, then
    repeat with `acknowledgeUnsupported: true`). The old per-watch knobs are refused with 422 naming the
    field in `error.field`, from the first call: cooldownS, kind, rearmS, recheckS, minConfidence,
    notWhen, zones, concerns, judgeKey, interpret, and runtime: core.

    Args:
        body (CreateWatchBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CreateWatchResponse201, CreateWatchResponse422, Error]
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
