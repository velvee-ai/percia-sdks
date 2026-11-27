from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_watch_draft_body import CreateWatchDraftBody
from ...models.create_watch_draft_response_201 import CreateWatchDraftResponse201
from ...models.error import Error
from ...types import Response


def _get_kwargs(
    *,
    body: CreateWatchDraftBody,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/watches/draft",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[CreateWatchDraftResponse201, Error]]:
    if response.status_code == 201:
        response_201 = CreateWatchDraftResponse201.from_dict(response.json())

        return response_201

    if response.status_code == 400:
        response_400 = Error.from_dict(response.json())

        return response_400

    if response.status_code == 402:
        response_402 = Error.from_dict(response.json())

        return response_402

    if response.status_code == 404:
        response_404 = Error.from_dict(response.json())

        return response_404

    if response.status_code == 422:
        response_422 = Error.from_dict(response.json())

        return response_422

    if response.status_code == 503:
        response_503 = Error.from_dict(response.json())

        return response_503

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[CreateWatchDraftResponse201, Error]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: CreateWatchDraftBody,
) -> Response[Union[CreateWatchDraftResponse201, Error]]:
    """Start a watch the clarifying way (Percia). Send the plain ask and the camera (`cameraId` of one of
    your cameras, or a public `sourceUrl`). Percia's intelligence layer reads it and answers with a
    draft: `status` clarifying (ask the person `question`; `options` are numbered meanings they may pick
    by number or replace with their own words), ready (conditions understood: create the watch with POST
    /watches/owned {draftId, sourceUrl}), or refused (nothing visible is left to watch). `unsupported`
    lists parts that cannot be watched (audio, several cameras, who someone is: `refused` true); when
    `needsAcknowledgement` is true tell the person, then create with `acknowledgeUnsupported: true`.
    Nothing is created yet.

    Args:
        body (CreateWatchDraftBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CreateWatchDraftResponse201, Error]]
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
    body: CreateWatchDraftBody,
) -> Optional[Union[CreateWatchDraftResponse201, Error]]:
    """Start a watch the clarifying way (Percia). Send the plain ask and the camera (`cameraId` of one of
    your cameras, or a public `sourceUrl`). Percia's intelligence layer reads it and answers with a
    draft: `status` clarifying (ask the person `question`; `options` are numbered meanings they may pick
    by number or replace with their own words), ready (conditions understood: create the watch with POST
    /watches/owned {draftId, sourceUrl}), or refused (nothing visible is left to watch). `unsupported`
    lists parts that cannot be watched (audio, several cameras, who someone is: `refused` true); when
    `needsAcknowledgement` is true tell the person, then create with `acknowledgeUnsupported: true`.
    Nothing is created yet.

    Args:
        body (CreateWatchDraftBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CreateWatchDraftResponse201, Error]
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: CreateWatchDraftBody,
) -> Response[Union[CreateWatchDraftResponse201, Error]]:
    """Start a watch the clarifying way (Percia). Send the plain ask and the camera (`cameraId` of one of
    your cameras, or a public `sourceUrl`). Percia's intelligence layer reads it and answers with a
    draft: `status` clarifying (ask the person `question`; `options` are numbered meanings they may pick
    by number or replace with their own words), ready (conditions understood: create the watch with POST
    /watches/owned {draftId, sourceUrl}), or refused (nothing visible is left to watch). `unsupported`
    lists parts that cannot be watched (audio, several cameras, who someone is: `refused` true); when
    `needsAcknowledgement` is true tell the person, then create with `acknowledgeUnsupported: true`.
    Nothing is created yet.

    Args:
        body (CreateWatchDraftBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CreateWatchDraftResponse201, Error]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: CreateWatchDraftBody,
) -> Optional[Union[CreateWatchDraftResponse201, Error]]:
    """Start a watch the clarifying way (Percia). Send the plain ask and the camera (`cameraId` of one of
    your cameras, or a public `sourceUrl`). Percia's intelligence layer reads it and answers with a
    draft: `status` clarifying (ask the person `question`; `options` are numbered meanings they may pick
    by number or replace with their own words), ready (conditions understood: create the watch with POST
    /watches/owned {draftId, sourceUrl}), or refused (nothing visible is left to watch). `unsupported`
    lists parts that cannot be watched (audio, several cameras, who someone is: `refused` true); when
    `needsAcknowledgement` is true tell the person, then create with `acknowledgeUnsupported: true`.
    Nothing is created yet.

    Args:
        body (CreateWatchDraftBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CreateWatchDraftResponse201, Error]
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
