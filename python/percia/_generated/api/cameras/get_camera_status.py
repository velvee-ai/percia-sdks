from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.get_camera_status_response_200 import GetCameraStatusResponse200
from ...types import Response


def _get_kwargs(
    id: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/cameras/{id}/status".format(
            id=id,
        ),
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Error, GetCameraStatusResponse200]]:
    if response.status_code == 200:
        response_200 = GetCameraStatusResponse200.from_dict(response.json())

        return response_200

    if response.status_code == 401:
        response_401 = Error.from_dict(response.json())

        return response_401

    if response.status_code == 404:
        response_404 = Error.from_dict(response.json())

        return response_404

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Error, GetCameraStatusResponse200]]:
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
) -> Response[Union[Error, GetCameraStatusResponse200]]:
    """Poll one camera: state waiting (never published), online, offline or revoked, lastSeenAt,
    secondsSinceSeen and a hint with the likely reason and next step. Online means a heartbeat or
    allowed publish under 60 s ago. Codec, resolution and bitrate are not available (media server API is
    off).

    Args:
        id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, GetCameraStatusResponse200]]
    """

    kwargs = _get_kwargs(
        id=id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    id: str,
    *,
    client: AuthenticatedClient,
) -> Optional[Union[Error, GetCameraStatusResponse200]]:
    """Poll one camera: state waiting (never published), online, offline or revoked, lastSeenAt,
    secondsSinceSeen and a hint with the likely reason and next step. Online means a heartbeat or
    allowed publish under 60 s ago. Codec, resolution and bitrate are not available (media server API is
    off).

    Args:
        id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, GetCameraStatusResponse200]
    """

    return sync_detailed(
        id=id,
        client=client,
    ).parsed


async def asyncio_detailed(
    id: str,
    *,
    client: AuthenticatedClient,
) -> Response[Union[Error, GetCameraStatusResponse200]]:
    """Poll one camera: state waiting (never published), online, offline or revoked, lastSeenAt,
    secondsSinceSeen and a hint with the likely reason and next step. Online means a heartbeat or
    allowed publish under 60 s ago. Codec, resolution and bitrate are not available (media server API is
    off).

    Args:
        id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, GetCameraStatusResponse200]]
    """

    kwargs = _get_kwargs(
        id=id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    id: str,
    *,
    client: AuthenticatedClient,
) -> Optional[Union[Error, GetCameraStatusResponse200]]:
    """Poll one camera: state waiting (never published), online, offline or revoked, lastSeenAt,
    secondsSinceSeen and a hint with the likely reason and next step. Online means a heartbeat or
    allowed publish under 60 s ago. Codec, resolution and bitrate are not available (media server API is
    off).

    Args:
        id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, GetCameraStatusResponse200]
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
        )
    ).parsed
