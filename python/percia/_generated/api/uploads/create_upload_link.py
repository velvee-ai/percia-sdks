from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_upload_link_response_201 import CreateUploadLinkResponse201
from ...models.error import Error
from ...types import Response


def _get_kwargs() -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/uploads/link",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[CreateUploadLinkResponse201, Error]]:
    if response.status_code == 201:
        response_201 = CreateUploadLinkResponse201.from_dict(response.json())

        return response_201

    if response.status_code == 401:
        response_401 = Error.from_dict(response.json())

        return response_401

    if response.status_code == 402:
        response_402 = Error.from_dict(response.json())

        return response_402

    if response.status_code == 404:
        response_404 = Error.from_dict(response.json())

        return response_404

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[CreateUploadLinkResponse201, Error]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
) -> Response[Union[CreateUploadLinkResponse201, Error]]:
    """Make a short-lived upload page for a video file on the person's own device (for MCP agents, which
    cannot send bytes). No body. Returns `uploadUrl` (valid 30 minutes, no sign-in needed on it): show
    it to the person with show_link, never as plain text. They pick the file on that page and it uploads
    and is checked. When they say it is done, GET /uploads and take the newest file with `status: ready`
    and `createdAt` after the link's `createdAt`: its `source` (`percia-file://<id>`) is the `sourceUrl`
    for POST /watches/owned. 404 while video files are off.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CreateUploadLinkResponse201, Error]]
    """

    kwargs = _get_kwargs()

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
) -> Optional[Union[CreateUploadLinkResponse201, Error]]:
    """Make a short-lived upload page for a video file on the person's own device (for MCP agents, which
    cannot send bytes). No body. Returns `uploadUrl` (valid 30 minutes, no sign-in needed on it): show
    it to the person with show_link, never as plain text. They pick the file on that page and it uploads
    and is checked. When they say it is done, GET /uploads and take the newest file with `status: ready`
    and `createdAt` after the link's `createdAt`: its `source` (`percia-file://<id>`) is the `sourceUrl`
    for POST /watches/owned. 404 while video files are off.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CreateUploadLinkResponse201, Error]
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
) -> Response[Union[CreateUploadLinkResponse201, Error]]:
    """Make a short-lived upload page for a video file on the person's own device (for MCP agents, which
    cannot send bytes). No body. Returns `uploadUrl` (valid 30 minutes, no sign-in needed on it): show
    it to the person with show_link, never as plain text. They pick the file on that page and it uploads
    and is checked. When they say it is done, GET /uploads and take the newest file with `status: ready`
    and `createdAt` after the link's `createdAt`: its `source` (`percia-file://<id>`) is the `sourceUrl`
    for POST /watches/owned. 404 while video files are off.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CreateUploadLinkResponse201, Error]]
    """

    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
) -> Optional[Union[CreateUploadLinkResponse201, Error]]:
    """Make a short-lived upload page for a video file on the person's own device (for MCP agents, which
    cannot send bytes). No body. Returns `uploadUrl` (valid 30 minutes, no sign-in needed on it): show
    it to the person with show_link, never as plain text. They pick the file on that page and it uploads
    and is checked. When they say it is done, GET /uploads and take the newest file with `status: ready`
    and `createdAt` after the link's `createdAt`: its `source` (`percia-file://<id>`) is the `sourceUrl`
    for POST /watches/owned. 404 while video files are off.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CreateUploadLinkResponse201, Error]
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
