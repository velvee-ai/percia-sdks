from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.get_quality_tests_response_200 import GetQualityTestsResponse200
from ...types import Response


def _get_kwargs() -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/quality/tests",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Error, GetQualityTestsResponse200]]:
    if response.status_code == 200:
        response_200 = GetQualityTestsResponse200.from_dict(response.json())

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
) -> Response[Union[Error, GetQualityTestsResponse200]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
) -> Response[Union[Error, GetQualityTestsResponse200]]:
    """The test side of Quality: ground-truth clips (total and across how many watches), tests started in
    the last 7 days, and per watch its clip count and the scores of its last finished test (`caught`,
    `falseAlarms` as value/of, or null when unmeasured).

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, GetQualityTestsResponse200]]
    """

    kwargs = _get_kwargs()

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
) -> Optional[Union[Error, GetQualityTestsResponse200]]:
    """The test side of Quality: ground-truth clips (total and across how many watches), tests started in
    the last 7 days, and per watch its clip count and the scores of its last finished test (`caught`,
    `falseAlarms` as value/of, or null when unmeasured).

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, GetQualityTestsResponse200]
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
) -> Response[Union[Error, GetQualityTestsResponse200]]:
    """The test side of Quality: ground-truth clips (total and across how many watches), tests started in
    the last 7 days, and per watch its clip count and the scores of its last finished test (`caught`,
    `falseAlarms` as value/of, or null when unmeasured).

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, GetQualityTestsResponse200]]
    """

    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
) -> Optional[Union[Error, GetQualityTestsResponse200]]:
    """The test side of Quality: ground-truth clips (total and across how many watches), tests started in
    the last 7 days, and per watch its clip count and the scores of its last finished test (`caught`,
    `falseAlarms` as value/of, or null when unmeasured).

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, GetQualityTestsResponse200]
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
