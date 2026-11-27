from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...types import Response


def _get_kwargs(
    test_id: str,
    clip_id: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/test-clips/{test_id}/{clip_id}".format(
            test_id=test_id,
            clip_id=clip_id,
        ),
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, Error]]:
    if response.status_code == 200:
        response_200 = cast(Any, None)
        return response_200

    if response.status_code == 404:
        response_404 = Error.from_dict(response.json())

        return response_404

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Any, Error]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    test_id: str,
    clip_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[Any, Error]]:
    """The signed, short-lived read of one dataset or uploaded clip for a running test, or (clipId arc-<n>)
    of one five minute range of the camera's archive for an earlier-time test (query exp and sig). Used
    by the pool's test job; the signature is the credential. Never cached.

    Args:
        test_id (str):
        clip_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, Error]]
    """

    kwargs = _get_kwargs(
        test_id=test_id,
        clip_id=clip_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    test_id: str,
    clip_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[Any, Error]]:
    """The signed, short-lived read of one dataset or uploaded clip for a running test, or (clipId arc-<n>)
    of one five minute range of the camera's archive for an earlier-time test (query exp and sig). Used
    by the pool's test job; the signature is the credential. Never cached.

    Args:
        test_id (str):
        clip_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, Error]
    """

    return sync_detailed(
        test_id=test_id,
        clip_id=clip_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    test_id: str,
    clip_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[Any, Error]]:
    """The signed, short-lived read of one dataset or uploaded clip for a running test, or (clipId arc-<n>)
    of one five minute range of the camera's archive for an earlier-time test (query exp and sig). Used
    by the pool's test job; the signature is the credential. Never cached.

    Args:
        test_id (str):
        clip_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, Error]]
    """

    kwargs = _get_kwargs(
        test_id=test_id,
        clip_id=clip_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    test_id: str,
    clip_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[Any, Error]]:
    """The signed, short-lived read of one dataset or uploaded clip for a running test, or (clipId arc-<n>)
    of one five minute range of the camera's archive for an earlier-time test (query exp and sig). Used
    by the pool's test job; the signature is the credential. Never cached.

    Args:
        test_id (str):
        clip_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, Error]
    """

    return (
        await asyncio_detailed(
            test_id=test_id,
            clip_id=clip_id,
            client=client,
        )
    ).parsed
