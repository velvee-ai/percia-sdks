from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.add_dataset_clip_from_link_body import AddDatasetClipFromLinkBody
from ...models.add_dataset_clip_from_link_response_201 import (
    AddDatasetClipFromLinkResponse201,
)
from ...models.error import Error
from ...types import Response


def _get_kwargs(
    id: str,
    *,
    body: AddDatasetClipFromLinkBody,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/watches/{id}/dataset/from-link".format(
            id=id,
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[AddDatasetClipFromLinkResponse201, Error]]:
    if response.status_code == 201:
        response_201 = AddDatasetClipFromLinkResponse201.from_dict(response.json())

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
) -> Response[Union[AddDatasetClipFromLinkResponse201, Error]]:
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
    body: AddDatasetClipFromLinkBody,
) -> Response[Union[AddDatasetClipFromLinkResponse201, Error]]:
    """Keep a video from a pasted link as a dataset clip: {url, label, note?}. Percia fetches the link once
    (a public https link straight to an MP4 or MOV, up to 32 MB and 120 s; no address numbers, no
    password in the link, at most three redirects, each checked again), stores the video sealed and does
    not keep the link. 20 links an hour per user.

    Args:
        id (str):
        body (AddDatasetClipFromLinkBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[AddDatasetClipFromLinkResponse201, Error]]
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
    body: AddDatasetClipFromLinkBody,
) -> Optional[Union[AddDatasetClipFromLinkResponse201, Error]]:
    """Keep a video from a pasted link as a dataset clip: {url, label, note?}. Percia fetches the link once
    (a public https link straight to an MP4 or MOV, up to 32 MB and 120 s; no address numbers, no
    password in the link, at most three redirects, each checked again), stores the video sealed and does
    not keep the link. 20 links an hour per user.

    Args:
        id (str):
        body (AddDatasetClipFromLinkBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[AddDatasetClipFromLinkResponse201, Error]
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
    body: AddDatasetClipFromLinkBody,
) -> Response[Union[AddDatasetClipFromLinkResponse201, Error]]:
    """Keep a video from a pasted link as a dataset clip: {url, label, note?}. Percia fetches the link once
    (a public https link straight to an MP4 or MOV, up to 32 MB and 120 s; no address numbers, no
    password in the link, at most three redirects, each checked again), stores the video sealed and does
    not keep the link. 20 links an hour per user.

    Args:
        id (str):
        body (AddDatasetClipFromLinkBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[AddDatasetClipFromLinkResponse201, Error]]
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
    body: AddDatasetClipFromLinkBody,
) -> Optional[Union[AddDatasetClipFromLinkResponse201, Error]]:
    """Keep a video from a pasted link as a dataset clip: {url, label, note?}. Percia fetches the link once
    (a public https link straight to an MP4 or MOV, up to 32 MB and 120 s; no address numbers, no
    password in the link, at most three redirects, each checked again), stores the video sealed and does
    not keep the link. 20 links an hour per user.

    Args:
        id (str):
        body (AddDatasetClipFromLinkBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[AddDatasetClipFromLinkResponse201, Error]
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
            body=body,
        )
    ).parsed
