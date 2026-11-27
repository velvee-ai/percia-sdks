from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.upload_from_url_body import UploadFromUrlBody
from ...models.upload_from_url_response_201 import UploadFromUrlResponse201
from ...types import Response


def _get_kwargs(
    *,
    body: UploadFromUrlBody,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/uploads/from-url",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Error, UploadFromUrlResponse201]]:
    if response.status_code == 201:
        response_201 = UploadFromUrlResponse201.from_dict(response.json())

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

    if response.status_code == 413:
        response_413 = Error.from_dict(response.json())

        return response_413

    if response.status_code == 429:
        response_429 = Error.from_dict(response.json())

        return response_429

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Error, UploadFromUrlResponse201]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: UploadFromUrlBody,
) -> Response[Union[Error, UploadFromUrlResponse201]]:
    """Make a video file from a public https URL (for MCP agents, which cannot send bytes). Percia fetches
    it itself, one request: public https only (no IP addresses, private or internal names, user names or
    odd ports; each redirect is checked again), content type must be a video (mp4, mov, webm, mkv) or a
    generic binary with a video file name, and the same size and length limits as an upload apply (400
    invalid_url, 400 unsupported_type, 400 fetch_failed, 413 too_large, 400 too_long, bad_container,
    bad_codec, 429 upload_limit). Returns the ready upload: `uploadId` (= `id`) and `source` (`percia-
    file://<uploadId>`), which you pass as `sourceUrl` to POST /watches/owned. 404 while video files are
    off.

    Args:
        body (UploadFromUrlBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, UploadFromUrlResponse201]]
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
    body: UploadFromUrlBody,
) -> Optional[Union[Error, UploadFromUrlResponse201]]:
    """Make a video file from a public https URL (for MCP agents, which cannot send bytes). Percia fetches
    it itself, one request: public https only (no IP addresses, private or internal names, user names or
    odd ports; each redirect is checked again), content type must be a video (mp4, mov, webm, mkv) or a
    generic binary with a video file name, and the same size and length limits as an upload apply (400
    invalid_url, 400 unsupported_type, 400 fetch_failed, 413 too_large, 400 too_long, bad_container,
    bad_codec, 429 upload_limit). Returns the ready upload: `uploadId` (= `id`) and `source` (`percia-
    file://<uploadId>`), which you pass as `sourceUrl` to POST /watches/owned. 404 while video files are
    off.

    Args:
        body (UploadFromUrlBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, UploadFromUrlResponse201]
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: UploadFromUrlBody,
) -> Response[Union[Error, UploadFromUrlResponse201]]:
    """Make a video file from a public https URL (for MCP agents, which cannot send bytes). Percia fetches
    it itself, one request: public https only (no IP addresses, private or internal names, user names or
    odd ports; each redirect is checked again), content type must be a video (mp4, mov, webm, mkv) or a
    generic binary with a video file name, and the same size and length limits as an upload apply (400
    invalid_url, 400 unsupported_type, 400 fetch_failed, 413 too_large, 400 too_long, bad_container,
    bad_codec, 429 upload_limit). Returns the ready upload: `uploadId` (= `id`) and `source` (`percia-
    file://<uploadId>`), which you pass as `sourceUrl` to POST /watches/owned. 404 while video files are
    off.

    Args:
        body (UploadFromUrlBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, UploadFromUrlResponse201]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: UploadFromUrlBody,
) -> Optional[Union[Error, UploadFromUrlResponse201]]:
    """Make a video file from a public https URL (for MCP agents, which cannot send bytes). Percia fetches
    it itself, one request: public https only (no IP addresses, private or internal names, user names or
    odd ports; each redirect is checked again), content type must be a video (mp4, mov, webm, mkv) or a
    generic binary with a video file name, and the same size and length limits as an upload apply (400
    invalid_url, 400 unsupported_type, 400 fetch_failed, 413 too_large, 400 too_long, bad_container,
    bad_codec, 429 upload_limit). Returns the ready upload: `uploadId` (= `id`) and `source` (`percia-
    file://<uploadId>`), which you pass as `sourceUrl` to POST /watches/owned. 404 while video files are
    off.

    Args:
        body (UploadFromUrlBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, UploadFromUrlResponse201]
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
