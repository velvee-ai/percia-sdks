from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...types import UNSET, Response, Unset


def _get_kwargs(
    service: str,
    *,
    code: Union[Unset, str] = UNSET,
    state: Union[Unset, str] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["code"] = code

    params["state"] = state

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/integrations/callback/{service}".format(
            service=service,
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, Error]]:
    if response.status_code == 302:
        response_302 = cast(Any, None)
        return response_302

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
) -> Response[Union[Any, Error]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    service: str,
    *,
    client: AuthenticatedClient,
    code: Union[Unset, str] = UNSET,
    state: Union[Unset, str] = UNSET,
) -> Response[Union[Any, Error]]:
    """Where Slack and Discord return the browser (session only). Redirects to
    /integrations?connected=<service> or ?connect_error=<code>.

    Args:
        service (str):
        code (Union[Unset, str]):
        state (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, Error]]
    """

    kwargs = _get_kwargs(
        service=service,
        code=code,
        state=state,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    service: str,
    *,
    client: AuthenticatedClient,
    code: Union[Unset, str] = UNSET,
    state: Union[Unset, str] = UNSET,
) -> Optional[Union[Any, Error]]:
    """Where Slack and Discord return the browser (session only). Redirects to
    /integrations?connected=<service> or ?connect_error=<code>.

    Args:
        service (str):
        code (Union[Unset, str]):
        state (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, Error]
    """

    return sync_detailed(
        service=service,
        client=client,
        code=code,
        state=state,
    ).parsed


async def asyncio_detailed(
    service: str,
    *,
    client: AuthenticatedClient,
    code: Union[Unset, str] = UNSET,
    state: Union[Unset, str] = UNSET,
) -> Response[Union[Any, Error]]:
    """Where Slack and Discord return the browser (session only). Redirects to
    /integrations?connected=<service> or ?connect_error=<code>.

    Args:
        service (str):
        code (Union[Unset, str]):
        state (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, Error]]
    """

    kwargs = _get_kwargs(
        service=service,
        code=code,
        state=state,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    service: str,
    *,
    client: AuthenticatedClient,
    code: Union[Unset, str] = UNSET,
    state: Union[Unset, str] = UNSET,
) -> Optional[Union[Any, Error]]:
    """Where Slack and Discord return the browser (session only). Redirects to
    /integrations?connected=<service> or ?connect_error=<code>.

    Args:
        service (str):
        code (Union[Unset, str]):
        state (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, Error]
    """

    return (
        await asyncio_detailed(
            service=service,
            client=client,
            code=code,
            state=state,
        )
    ).parsed
