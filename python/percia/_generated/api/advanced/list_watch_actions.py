from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.list_watch_actions_response_200 import ListWatchActionsResponse200
from ...types import UNSET, Response, Unset


def _get_kwargs(
    id: str,
    *,
    limit: Union[Unset, int] = UNSET,
    cursor: Union[Unset, str] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["limit"] = limit

    params["cursor"] = cursor

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/watches/{id}/actions".format(
            id=id,
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Error, ListWatchActionsResponse200]]:
    if response.status_code == 200:
        response_200 = ListWatchActionsResponse200.from_dict(response.json())

        return response_200

    if response.status_code == 401:
        response_401 = Error.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = Error.from_dict(response.json())

        return response_403

    if response.status_code == 404:
        response_404 = Error.from_dict(response.json())

        return response_404

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Error, ListWatchActionsResponse200]]:
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
    limit: Union[Unset, int] = UNSET,
    cursor: Union[Unset, str] = UNSET,
) -> Response[Union[Error, ListWatchActionsResponse200]]:
    """The typed recommendations (ActionEvent) the engine made for an advanced watch, newest first

     The typed recommendations (pause, stop, inspect, adjust, resume_ok) the engine made for a watch made
    with `advanced`. Percia recommends, you decide. Webhook watches also receive each one as
    `percia.action`.

    Args:
        id (str):
        limit (Union[Unset, int]):
        cursor (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, ListWatchActionsResponse200]]
    """

    kwargs = _get_kwargs(
        id=id,
        limit=limit,
        cursor=cursor,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    id: str,
    *,
    client: AuthenticatedClient,
    limit: Union[Unset, int] = UNSET,
    cursor: Union[Unset, str] = UNSET,
) -> Optional[Union[Error, ListWatchActionsResponse200]]:
    """The typed recommendations (ActionEvent) the engine made for an advanced watch, newest first

     The typed recommendations (pause, stop, inspect, adjust, resume_ok) the engine made for a watch made
    with `advanced`. Percia recommends, you decide. Webhook watches also receive each one as
    `percia.action`.

    Args:
        id (str):
        limit (Union[Unset, int]):
        cursor (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, ListWatchActionsResponse200]
    """

    return sync_detailed(
        id=id,
        client=client,
        limit=limit,
        cursor=cursor,
    ).parsed


async def asyncio_detailed(
    id: str,
    *,
    client: AuthenticatedClient,
    limit: Union[Unset, int] = UNSET,
    cursor: Union[Unset, str] = UNSET,
) -> Response[Union[Error, ListWatchActionsResponse200]]:
    """The typed recommendations (ActionEvent) the engine made for an advanced watch, newest first

     The typed recommendations (pause, stop, inspect, adjust, resume_ok) the engine made for a watch made
    with `advanced`. Percia recommends, you decide. Webhook watches also receive each one as
    `percia.action`.

    Args:
        id (str):
        limit (Union[Unset, int]):
        cursor (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, ListWatchActionsResponse200]]
    """

    kwargs = _get_kwargs(
        id=id,
        limit=limit,
        cursor=cursor,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    id: str,
    *,
    client: AuthenticatedClient,
    limit: Union[Unset, int] = UNSET,
    cursor: Union[Unset, str] = UNSET,
) -> Optional[Union[Error, ListWatchActionsResponse200]]:
    """The typed recommendations (ActionEvent) the engine made for an advanced watch, newest first

     The typed recommendations (pause, stop, inspect, adjust, resume_ok) the engine made for a watch made
    with `advanced`. Percia recommends, you decide. Webhook watches also receive each one as
    `percia.action`.

    Args:
        id (str):
        limit (Union[Unset, int]):
        cursor (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, ListWatchActionsResponse200]
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
            limit=limit,
            cursor=cursor,
        )
    ).parsed
