from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.start_test_run_body import StartTestRunBody
from ...models.start_test_run_response_201 import StartTestRunResponse201
from ...types import Response


def _get_kwargs(
    id: str,
    *,
    body: StartTestRunBody,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/watches/{id}/tests".format(
            id=id,
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Error, StartTestRunResponse201]]:
    if response.status_code == 201:
        response_201 = StartTestRunResponse201.from_dict(response.json())

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

    if response.status_code == 409:
        response_409 = Error.from_dict(response.json())

        return response_409

    if response.status_code == 413:
        response_413 = Error.from_dict(response.json())

        return response_413

    if response.status_code == 429:
        response_429 = Error.from_dict(response.json())

        return response_429

    if response.status_code == 503:
        response_503 = Error.from_dict(response.json())

        return response_503

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Error, StartTestRunResponse201]]:
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
    body: StartTestRunBody,
) -> Response[Union[Error, StartTestRunResponse201]]:
    r"""Start a test. JSON {source: \"recent\", minutes?: 1..10} replays the camera's last minutes, {source:
    \"window\", from, minutes?: 1..10} an earlier time (up to 14 days back, ending at least a minute
    ago; the host's recording for about two hours, the sealed archive beyond that), {source:
    \"dataset\"} replays the dataset clips (the newest 40) and scores them: Caught = should_match clips
    the judge said yes on, False alarms = should_not and counterfactual clips it said yes on. Or
    multipart/form-data with `file` tests one uploaded clip (deleted afterwards; no labels, so no
    scores, only what it would alert on). Uses the pool's judge at half the camera's hourly cap. 10
    tests an hour per user, one at a time per watch.

    Args:
        id (str):
        body (StartTestRunBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, StartTestRunResponse201]]
    """

    kwargs = _get_kwargs(
        id=id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    id: str,
    *,
    client: AuthenticatedClient,
    body: StartTestRunBody,
) -> Optional[Union[Error, StartTestRunResponse201]]:
    r"""Start a test. JSON {source: \"recent\", minutes?: 1..10} replays the camera's last minutes, {source:
    \"window\", from, minutes?: 1..10} an earlier time (up to 14 days back, ending at least a minute
    ago; the host's recording for about two hours, the sealed archive beyond that), {source:
    \"dataset\"} replays the dataset clips (the newest 40) and scores them: Caught = should_match clips
    the judge said yes on, False alarms = should_not and counterfactual clips it said yes on. Or
    multipart/form-data with `file` tests one uploaded clip (deleted afterwards; no labels, so no
    scores, only what it would alert on). Uses the pool's judge at half the camera's hourly cap. 10
    tests an hour per user, one at a time per watch.

    Args:
        id (str):
        body (StartTestRunBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, StartTestRunResponse201]
    """

    return sync_detailed(
        id=id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    id: str,
    *,
    client: AuthenticatedClient,
    body: StartTestRunBody,
) -> Response[Union[Error, StartTestRunResponse201]]:
    r"""Start a test. JSON {source: \"recent\", minutes?: 1..10} replays the camera's last minutes, {source:
    \"window\", from, minutes?: 1..10} an earlier time (up to 14 days back, ending at least a minute
    ago; the host's recording for about two hours, the sealed archive beyond that), {source:
    \"dataset\"} replays the dataset clips (the newest 40) and scores them: Caught = should_match clips
    the judge said yes on, False alarms = should_not and counterfactual clips it said yes on. Or
    multipart/form-data with `file` tests one uploaded clip (deleted afterwards; no labels, so no
    scores, only what it would alert on). Uses the pool's judge at half the camera's hourly cap. 10
    tests an hour per user, one at a time per watch.

    Args:
        id (str):
        body (StartTestRunBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, StartTestRunResponse201]]
    """

    kwargs = _get_kwargs(
        id=id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    id: str,
    *,
    client: AuthenticatedClient,
    body: StartTestRunBody,
) -> Optional[Union[Error, StartTestRunResponse201]]:
    r"""Start a test. JSON {source: \"recent\", minutes?: 1..10} replays the camera's last minutes, {source:
    \"window\", from, minutes?: 1..10} an earlier time (up to 14 days back, ending at least a minute
    ago; the host's recording for about two hours, the sealed archive beyond that), {source:
    \"dataset\"} replays the dataset clips (the newest 40) and scores them: Caught = should_match clips
    the judge said yes on, False alarms = should_not and counterfactual clips it said yes on. Or
    multipart/form-data with `file` tests one uploaded clip (deleted afterwards; no labels, so no
    scores, only what it would alert on). Uses the pool's judge at half the camera's hourly cap. 10
    tests an hour per user, one at a time per watch.

    Args:
        id (str):
        body (StartTestRunBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, StartTestRunResponse201]
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
            body=body,
        )
    ).parsed
