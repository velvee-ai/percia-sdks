from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.image_link import ImageLink
from ...types import Response


def _get_kwargs(
    case_id: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/tests/{case_id}/image/link".format(
            case_id=case_id,
        ),
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Error, ImageLink]]:
    if response.status_code == 200:
        response_200 = ImageLink.from_dict(response.json())

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
) -> Response[Union[Error, ImageLink]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    case_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[Union[Error, ImageLink]]:
    """A 10 minute link to the test case image that needs no credential (see /img/:token). Needs
    events:read with an API key.

    Args:
        case_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, ImageLink]]
    """

    kwargs = _get_kwargs(
        case_id=case_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    case_id: str,
    *,
    client: AuthenticatedClient,
) -> Optional[Union[Error, ImageLink]]:
    """A 10 minute link to the test case image that needs no credential (see /img/:token). Needs
    events:read with an API key.

    Args:
        case_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, ImageLink]
    """

    return sync_detailed(
        case_id=case_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    case_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[Union[Error, ImageLink]]:
    """A 10 minute link to the test case image that needs no credential (see /img/:token). Needs
    events:read with an API key.

    Args:
        case_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, ImageLink]]
    """

    kwargs = _get_kwargs(
        case_id=case_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    case_id: str,
    *,
    client: AuthenticatedClient,
) -> Optional[Union[Error, ImageLink]]:
    """A 10 minute link to the test case image that needs no credential (see /img/:token). Needs
    events:read with an API key.

    Args:
        case_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, ImageLink]
    """

    return (
        await asyncio_detailed(
            case_id=case_id,
            client=client,
        )
    ).parsed
