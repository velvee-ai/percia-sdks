from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_watch_body import CreateWatchBody
from ...models.create_watch_response_201 import CreateWatchResponse201
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
) -> Optional[Union[CreateWatchResponse201, Error]]:
    if response.status_code == 201:
        response_201 = CreateWatchResponse201.from_dict(response.json())

        return response_201

    if response.status_code == 400:
        response_400 = Error.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = Error.from_dict(response.json())

        return response_401

    if response.status_code == 429:
        response_429 = Error.from_dict(response.json())

        return response_429

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[CreateWatchResponse201, Error]]:
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
) -> Response[Union[CreateWatchResponse201, Error]]:
    """Create a watch as the signed-in user (email or webhook; no Turnstile). sourceUrl may be percia-
    cam://<cameraId> for one of your own phone cameras. Send `goal`, or `agentId` (+ optional
    `agentVersion`; omitted = follow the latest) to deploy a published agent.

    Args:
        body (CreateWatchBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CreateWatchResponse201, Error]]
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
) -> Optional[Union[CreateWatchResponse201, Error]]:
    """Create a watch as the signed-in user (email or webhook; no Turnstile). sourceUrl may be percia-
    cam://<cameraId> for one of your own phone cameras. Send `goal`, or `agentId` (+ optional
    `agentVersion`; omitted = follow the latest) to deploy a published agent.

    Args:
        body (CreateWatchBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CreateWatchResponse201, Error]
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: CreateWatchBody,
) -> Response[Union[CreateWatchResponse201, Error]]:
    """Create a watch as the signed-in user (email or webhook; no Turnstile). sourceUrl may be percia-
    cam://<cameraId> for one of your own phone cameras. Send `goal`, or `agentId` (+ optional
    `agentVersion`; omitted = follow the latest) to deploy a published agent.

    Args:
        body (CreateWatchBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CreateWatchResponse201, Error]]
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
) -> Optional[Union[CreateWatchResponse201, Error]]:
    """Create a watch as the signed-in user (email or webhook; no Turnstile). sourceUrl may be percia-
    cam://<cameraId> for one of your own phone cameras. Send `goal`, or `agentId` (+ optional
    `agentVersion`; omitted = follow the latest) to deploy a published agent.

    Args:
        body (CreateWatchBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CreateWatchResponse201, Error]
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
