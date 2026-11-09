from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.get_usage_response_200 import GetUsageResponse200
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    days: Union[Unset, int] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["days"] = days

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/usage",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Error, GetUsageResponse200]]:
    if response.status_code == 200:
        response_200 = GetUsageResponse200.from_dict(response.json())

        return response_200

    if response.status_code == 401:
        response_401 = Error.from_dict(response.json())

        return response_401

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Error, GetUsageResponse200]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    days: Union[Unset, int] = UNSET,
) -> Response[Union[Error, GetUsageResponse200]]:
    """Daily usage (UTC days): active watch-hours, events, model calls (and how many used your own key) and
    action calls

    Args:
        days (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, GetUsageResponse200]]
    """

    kwargs = _get_kwargs(
        days=days,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    days: Union[Unset, int] = UNSET,
) -> Optional[Union[Error, GetUsageResponse200]]:
    """Daily usage (UTC days): active watch-hours, events, model calls (and how many used your own key) and
    action calls

    Args:
        days (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, GetUsageResponse200]
    """

    return sync_detailed(
        client=client,
        days=days,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    days: Union[Unset, int] = UNSET,
) -> Response[Union[Error, GetUsageResponse200]]:
    """Daily usage (UTC days): active watch-hours, events, model calls (and how many used your own key) and
    action calls

    Args:
        days (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, GetUsageResponse200]]
    """

    kwargs = _get_kwargs(
        days=days,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    days: Union[Unset, int] = UNSET,
) -> Optional[Union[Error, GetUsageResponse200]]:
    """Daily usage (UTC days): active watch-hours, events, model calls (and how many used your own key) and
    action calls

    Args:
        days (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, GetUsageResponse200]
    """

    return (
        await asyncio_detailed(
            client=client,
            days=days,
        )
    ).parsed
