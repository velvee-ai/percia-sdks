from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.get_test_run_response_200 import GetTestRunResponse200
from ...types import Response


def _get_kwargs(
    id: str,
    test_id: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/watches/{id}/tests/{test_id}".format(
            id=id,
            test_id=test_id,
        ),
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Error, GetTestRunResponse200]]:
    if response.status_code == 200:
        response_200 = GetTestRunResponse200.from_dict(response.json())

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
) -> Response[Union[Error, GetTestRunResponse200]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: str,
    test_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[Union[Error, GetTestRunResponse200]]:
    """One test run. While it runs, `status` is running and there are no scores; when it ends, `scores` has
    Caught, False alarms, Avg delay and Verdict (each a figure with its total, or null with a note
    saying why it is unmeasured), the clips' outcomes, the alerts a window test found, coverage and the
    per-condition capability report.

    Args:
        id (str):
        test_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, GetTestRunResponse200]]
    """

    kwargs = _get_kwargs(
        id=id,
        test_id=test_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    id: str,
    test_id: str,
    *,
    client: AuthenticatedClient,
) -> Optional[Union[Error, GetTestRunResponse200]]:
    """One test run. While it runs, `status` is running and there are no scores; when it ends, `scores` has
    Caught, False alarms, Avg delay and Verdict (each a figure with its total, or null with a note
    saying why it is unmeasured), the clips' outcomes, the alerts a window test found, coverage and the
    per-condition capability report.

    Args:
        id (str):
        test_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, GetTestRunResponse200]
    """

    return sync_detailed(
        id=id,
        test_id=test_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    id: str,
    test_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[Union[Error, GetTestRunResponse200]]:
    """One test run. While it runs, `status` is running and there are no scores; when it ends, `scores` has
    Caught, False alarms, Avg delay and Verdict (each a figure with its total, or null with a note
    saying why it is unmeasured), the clips' outcomes, the alerts a window test found, coverage and the
    per-condition capability report.

    Args:
        id (str):
        test_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, GetTestRunResponse200]]
    """

    kwargs = _get_kwargs(
        id=id,
        test_id=test_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    id: str,
    test_id: str,
    *,
    client: AuthenticatedClient,
) -> Optional[Union[Error, GetTestRunResponse200]]:
    """One test run. While it runs, `status` is running and there are no scores; when it ends, `scores` has
    Caught, False alarms, Avg delay and Verdict (each a figure with its total, or null with a note
    saying why it is unmeasured), the clips' outcomes, the alerts a window test found, coverage and the
    per-condition capability report.

    Args:
        id (str):
        test_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, GetTestRunResponse200]
    """

    return (
        await asyncio_detailed(
            id=id,
            test_id=test_id,
            client=client,
        )
    ).parsed
