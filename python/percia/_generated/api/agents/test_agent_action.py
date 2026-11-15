from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.test_agent_action_response_200 import TestAgentActionResponse200
from ...types import Response


def _get_kwargs(
    id: str,
    index: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/agents/{id}/actions/{index}/test".format(
            id=id,
            index=index,
        ),
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Error, TestAgentActionResponse200]]:
    if response.status_code == 200:
        response_200 = TestAgentActionResponse200.from_dict(response.json())

        return response_200

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
) -> Response[Union[Error, TestAgentActionResponse200]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: str,
    index: str,
    *,
    client: AuthenticatedClient,
) -> Response[Union[Error, TestAgentActionResponse200]]:
    """Run one action of the draft against a sample event (counts toward 60 action calls per hour)

    Args:
        id (str):
        index (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, TestAgentActionResponse200]]
    """

    kwargs = _get_kwargs(
        id=id,
        index=index,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    id: str,
    index: str,
    *,
    client: AuthenticatedClient,
) -> Optional[Union[Error, TestAgentActionResponse200]]:
    """Run one action of the draft against a sample event (counts toward 60 action calls per hour)

    Args:
        id (str):
        index (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, TestAgentActionResponse200]
    """

    return sync_detailed(
        id=id,
        index=index,
        client=client,
    ).parsed


async def asyncio_detailed(
    id: str,
    index: str,
    *,
    client: AuthenticatedClient,
) -> Response[Union[Error, TestAgentActionResponse200]]:
    """Run one action of the draft against a sample event (counts toward 60 action calls per hour)

    Args:
        id (str):
        index (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, TestAgentActionResponse200]]
    """

    kwargs = _get_kwargs(
        id=id,
        index=index,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    id: str,
    index: str,
    *,
    client: AuthenticatedClient,
) -> Optional[Union[Error, TestAgentActionResponse200]]:
    """Run one action of the draft against a sample event (counts toward 60 action calls per hour)

    Args:
        id (str):
        index (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, TestAgentActionResponse200]
    """

    return (
        await asyncio_detailed(
            id=id,
            index=index,
            client=client,
        )
    ).parsed
