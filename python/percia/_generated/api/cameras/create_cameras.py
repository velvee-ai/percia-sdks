from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_cameras_body import CreateCamerasBody
from ...models.create_cameras_response_201 import CreateCamerasResponse201
from ...models.error import Error
from ...types import Response


def _get_kwargs(
    *,
    body: CreateCamerasBody,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/cameras/bulk",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, CreateCamerasResponse201, Error]]:
    if response.status_code == 200:
        response_200 = cast(Any, None)
        return response_200

    if response.status_code == 201:
        response_201 = CreateCamerasResponse201.from_dict(response.json())

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

    if response.status_code == 404:
        response_404 = Error.from_dict(response.json())

        return response_404

    if response.status_code == 429:
        response_429 = Error.from_dict(response.json())

        return response_429

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Any, CreateCamerasResponse201, Error]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: CreateCamerasBody,
) -> Response[Union[Any, CreateCamerasResponse201, Error]]:
    """Register up to 10 push cameras at once (an NVR connector). Each needs name and externalId and is
    idempotent by externalId (existing ones come back with token null). All or nothing against the
    10-camera limit (429 camera_limit, nothing created).

    Args:
        body (CreateCamerasBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, CreateCamerasResponse201, Error]]
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
    body: CreateCamerasBody,
) -> Optional[Union[Any, CreateCamerasResponse201, Error]]:
    """Register up to 10 push cameras at once (an NVR connector). Each needs name and externalId and is
    idempotent by externalId (existing ones come back with token null). All or nothing against the
    10-camera limit (429 camera_limit, nothing created).

    Args:
        body (CreateCamerasBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, CreateCamerasResponse201, Error]
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: CreateCamerasBody,
) -> Response[Union[Any, CreateCamerasResponse201, Error]]:
    """Register up to 10 push cameras at once (an NVR connector). Each needs name and externalId and is
    idempotent by externalId (existing ones come back with token null). All or nothing against the
    10-camera limit (429 camera_limit, nothing created).

    Args:
        body (CreateCamerasBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, CreateCamerasResponse201, Error]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: CreateCamerasBody,
) -> Optional[Union[Any, CreateCamerasResponse201, Error]]:
    """Register up to 10 push cameras at once (an NVR connector). Each needs name and externalId and is
    idempotent by externalId (existing ones come back with token null). All or nothing against the
    10-camera limit (429 camera_limit, nothing created).

    Args:
        body (CreateCamerasBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, CreateCamerasResponse201, Error]
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
