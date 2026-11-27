from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.upload_part_response_200 import UploadPartResponse200
from ...types import Response


def _get_kwargs(
    id: str,
    n: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/uploads/{id}/parts/{n}".format(
            id=id,
            n=n,
        ),
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Error, UploadPartResponse200]]:
    if response.status_code == 200:
        response_200 = UploadPartResponse200.from_dict(response.json())

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

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Error, UploadPartResponse200]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: str,
    n: str,
    *,
    client: AuthenticatedClient,
) -> Response[Union[Error, UploadPartResponse200]]:
    """Send part n (1-based) as the raw request body (application/octet-stream). Every part but the last is
    exactly `partSize` bytes. Returns the etag to give to /complete. A part may be sent again. Needs a
    client that can send bytes: MCP agents cannot, a person uses the app.

    Args:
        id (str):
        n (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, UploadPartResponse200]]
    """

    kwargs = _get_kwargs(
        id=id,
        n=n,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    id: str,
    n: str,
    *,
    client: AuthenticatedClient,
) -> Optional[Union[Error, UploadPartResponse200]]:
    """Send part n (1-based) as the raw request body (application/octet-stream). Every part but the last is
    exactly `partSize` bytes. Returns the etag to give to /complete. A part may be sent again. Needs a
    client that can send bytes: MCP agents cannot, a person uses the app.

    Args:
        id (str):
        n (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, UploadPartResponse200]
    """

    return sync_detailed(
        id=id,
        n=n,
        client=client,
    ).parsed


async def asyncio_detailed(
    id: str,
    n: str,
    *,
    client: AuthenticatedClient,
) -> Response[Union[Error, UploadPartResponse200]]:
    """Send part n (1-based) as the raw request body (application/octet-stream). Every part but the last is
    exactly `partSize` bytes. Returns the etag to give to /complete. A part may be sent again. Needs a
    client that can send bytes: MCP agents cannot, a person uses the app.

    Args:
        id (str):
        n (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, UploadPartResponse200]]
    """

    kwargs = _get_kwargs(
        id=id,
        n=n,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    id: str,
    n: str,
    *,
    client: AuthenticatedClient,
) -> Optional[Union[Error, UploadPartResponse200]]:
    """Send part n (1-based) as the raw request body (application/octet-stream). Every part but the last is
    exactly `partSize` bytes. Returns the etag to give to /complete. A part may be sent again. Needs a
    client that can send bytes: MCP agents cannot, a person uses the app.

    Args:
        id (str):
        n (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, UploadPartResponse200]
    """

    return (
        await asyncio_detailed(
            id=id,
            n=n,
            client=client,
        )
    ).parsed
