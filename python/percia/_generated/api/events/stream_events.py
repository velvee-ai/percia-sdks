from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    watch_id: Union[Unset, str] = UNSET,
    concern_id: Union[Unset, str] = UNSET,
    type_: Union[Unset, str] = UNSET,
    since: Union[Unset, str] = UNSET,
    client_query: Union[Unset, str] = UNSET,
    interval: Union[Unset, str] = UNSET,
    backlog: Union[Unset, int] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["watchId"] = watch_id

    params["concernId"] = concern_id

    params["type"] = type_

    params["since"] = since

    params["client"] = client_query

    params["interval"] = interval

    params["backlog"] = backlog

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/events/stream",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, Error]]:
    if response.status_code == 200:
        response_200 = cast(Any, None)
        return response_200

    if response.status_code == 400:
        response_400 = Error.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = Error.from_dict(response.json())

        return response_401

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
) -> Response[Union[Any, Error]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    watch_id: Union[Unset, str] = UNSET,
    concern_id: Union[Unset, str] = UNSET,
    type_: Union[Unset, str] = UNSET,
    since: Union[Unset, str] = UNSET,
    client_query: Union[Unset, str] = UNSET,
    interval: Union[Unset, str] = UNSET,
    backlog: Union[Unset, int] = UNSET,
) -> Response[Union[Any, Error]]:
    """Developer event feed: server-sent events of your account, for local development

    Args:
        watch_id (Union[Unset, str]):
        concern_id (Union[Unset, str]):
        type_ (Union[Unset, str]):
        since (Union[Unset, str]):
        client_query (Union[Unset, str]):
        interval (Union[Unset, str]):
        backlog (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, Error]]
    """

    kwargs = _get_kwargs(
        watch_id=watch_id,
        concern_id=concern_id,
        type_=type_,
        since=since,
        client_query=client_query,
        interval=interval,
        backlog=backlog,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    watch_id: Union[Unset, str] = UNSET,
    concern_id: Union[Unset, str] = UNSET,
    type_: Union[Unset, str] = UNSET,
    since: Union[Unset, str] = UNSET,
    client_query: Union[Unset, str] = UNSET,
    interval: Union[Unset, str] = UNSET,
    backlog: Union[Unset, int] = UNSET,
) -> Optional[Union[Any, Error]]:
    """Developer event feed: server-sent events of your account, for local development

    Args:
        watch_id (Union[Unset, str]):
        concern_id (Union[Unset, str]):
        type_ (Union[Unset, str]):
        since (Union[Unset, str]):
        client_query (Union[Unset, str]):
        interval (Union[Unset, str]):
        backlog (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, Error]
    """

    return sync_detailed(
        client=client,
        watch_id=watch_id,
        concern_id=concern_id,
        type_=type_,
        since=since,
        client_query=client_query,
        interval=interval,
        backlog=backlog,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    watch_id: Union[Unset, str] = UNSET,
    concern_id: Union[Unset, str] = UNSET,
    type_: Union[Unset, str] = UNSET,
    since: Union[Unset, str] = UNSET,
    client_query: Union[Unset, str] = UNSET,
    interval: Union[Unset, str] = UNSET,
    backlog: Union[Unset, int] = UNSET,
) -> Response[Union[Any, Error]]:
    """Developer event feed: server-sent events of your account, for local development

    Args:
        watch_id (Union[Unset, str]):
        concern_id (Union[Unset, str]):
        type_ (Union[Unset, str]):
        since (Union[Unset, str]):
        client_query (Union[Unset, str]):
        interval (Union[Unset, str]):
        backlog (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, Error]]
    """

    kwargs = _get_kwargs(
        watch_id=watch_id,
        concern_id=concern_id,
        type_=type_,
        since=since,
        client_query=client_query,
        interval=interval,
        backlog=backlog,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    watch_id: Union[Unset, str] = UNSET,
    concern_id: Union[Unset, str] = UNSET,
    type_: Union[Unset, str] = UNSET,
    since: Union[Unset, str] = UNSET,
    client_query: Union[Unset, str] = UNSET,
    interval: Union[Unset, str] = UNSET,
    backlog: Union[Unset, int] = UNSET,
) -> Optional[Union[Any, Error]]:
    """Developer event feed: server-sent events of your account, for local development

    Args:
        watch_id (Union[Unset, str]):
        concern_id (Union[Unset, str]):
        type_ (Union[Unset, str]):
        since (Union[Unset, str]):
        client_query (Union[Unset, str]):
        interval (Union[Unset, str]):
        backlog (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, Error]
    """

    return (
        await asyncio_detailed(
            client=client,
            watch_id=watch_id,
            concern_id=concern_id,
            type_=type_,
            since=since,
            client_query=client_query,
            interval=interval,
            backlog=backlog,
        )
    ).parsed
