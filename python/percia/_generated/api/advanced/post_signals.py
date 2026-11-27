from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.post_signals_body import PostSignalsBody
from ...models.post_signals_response_202 import PostSignalsResponse202
from ...types import Response


def _get_kwargs(
    *,
    body: PostSignalsBody,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/signals",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Error, PostSignalsResponse202]]:
    if response.status_code == 202:
        response_202 = PostSignalsResponse202.from_dict(response.json())

        return response_202

    if response.status_code == 400:
        response_400 = Error.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = Error.from_dict(response.json())

        return response_401

    if response.status_code == 402:
        response_402 = Error.from_dict(response.json())

        return response_402

    if response.status_code == 403:
        response_403 = Error.from_dict(response.json())

        return response_403

    if response.status_code == 404:
        response_404 = Error.from_dict(response.json())

        return response_404

    if response.status_code == 413:
        response_413 = Error.from_dict(response.json())

        return response_413

    if response.status_code == 422:
        response_422 = Error.from_dict(response.json())

        return response_422

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
) -> Response[Union[Error, PostSignalsResponse202]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: PostSignalsBody,
) -> Response[Union[Error, PostSignalsResponse202]]:
    """Send timed machine signals (Signal) for a camera or site (advanced)

     where recording is on only. Send timed samples from a machine: `{cameraId?, siteId?, signals:
    [{channel, t_utc, value, seq?, camera_id?, site_id?}]}` (Signal; leave out tenant_id). `t_utc` is
    the machine's clock in UTC: declare its offset, lag and latency in the site context (`signals[]`);
    the engine corrects time with them. A repeat of the same channel and `seq` is idempotent. At most
    200 signals and 64 KiB per request, 100 signals per second per camera (burst 500), nothing older
    than 6 hours. Declare a channel in the site context before a watch reads it. Needs scope
    signals:write.

    Args:
        body (PostSignalsBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, PostSignalsResponse202]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    body: PostSignalsBody,
) -> Optional[Union[Error, PostSignalsResponse202]]:
    """Send timed machine signals (Signal) for a camera or site (advanced)

     where recording is on only. Send timed samples from a machine: `{cameraId?, siteId?, signals:
    [{channel, t_utc, value, seq?, camera_id?, site_id?}]}` (Signal; leave out tenant_id). `t_utc` is
    the machine's clock in UTC: declare its offset, lag and latency in the site context (`signals[]`);
    the engine corrects time with them. A repeat of the same channel and `seq` is idempotent. At most
    200 signals and 64 KiB per request, 100 signals per second per camera (burst 500), nothing older
    than 6 hours. Declare a channel in the site context before a watch reads it. Needs scope
    signals:write.

    Args:
        body (PostSignalsBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, PostSignalsResponse202]
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: PostSignalsBody,
) -> Response[Union[Error, PostSignalsResponse202]]:
    """Send timed machine signals (Signal) for a camera or site (advanced)

     where recording is on only. Send timed samples from a machine: `{cameraId?, siteId?, signals:
    [{channel, t_utc, value, seq?, camera_id?, site_id?}]}` (Signal; leave out tenant_id). `t_utc` is
    the machine's clock in UTC: declare its offset, lag and latency in the site context (`signals[]`);
    the engine corrects time with them. A repeat of the same channel and `seq` is idempotent. At most
    200 signals and 64 KiB per request, 100 signals per second per camera (burst 500), nothing older
    than 6 hours. Declare a channel in the site context before a watch reads it. Needs scope
    signals:write.

    Args:
        body (PostSignalsBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, PostSignalsResponse202]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: PostSignalsBody,
) -> Optional[Union[Error, PostSignalsResponse202]]:
    """Send timed machine signals (Signal) for a camera or site (advanced)

     where recording is on only. Send timed samples from a machine: `{cameraId?, siteId?, signals:
    [{channel, t_utc, value, seq?, camera_id?, site_id?}]}` (Signal; leave out tenant_id). `t_utc` is
    the machine's clock in UTC: declare its offset, lag and latency in the site context (`signals[]`);
    the engine corrects time with them. A repeat of the same channel and `seq` is idempotent. At most
    200 signals and 64 KiB per request, 100 signals per second per camera (burst 500), nothing older
    than 6 hours. Declare a channel in the site context before a watch reads it. Needs scope
    signals:write.

    Args:
        body (PostSignalsBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, PostSignalsResponse202]
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
