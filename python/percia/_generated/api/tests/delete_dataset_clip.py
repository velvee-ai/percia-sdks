from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.delete_dataset_clip_response_200 import DeleteDatasetClipResponse200
from ...models.error import Error
from ...types import Response


def _get_kwargs(
    id: str,
    clip_id: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": "/watches/{id}/dataset/{clip_id}".format(
            id=id,
            clip_id=clip_id,
        ),
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[DeleteDatasetClipResponse200, Error]]:
    if response.status_code == 200:
        response_200 = DeleteDatasetClipResponse200.from_dict(response.json())

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
) -> Response[Union[DeleteDatasetClipResponse200, Error]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: str,
    clip_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[Union[DeleteDatasetClipResponse200, Error]]:
    """Delete a clip and its stored video. The dataset also goes with the watch and with the account.

    Args:
        id (str):
        clip_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DeleteDatasetClipResponse200, Error]]
    """

    kwargs = _get_kwargs(
        id=id,
        clip_id=clip_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    id: str,
    clip_id: str,
    *,
    client: AuthenticatedClient,
) -> Optional[Union[DeleteDatasetClipResponse200, Error]]:
    """Delete a clip and its stored video. The dataset also goes with the watch and with the account.

    Args:
        id (str):
        clip_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DeleteDatasetClipResponse200, Error]
    """

    return sync_detailed(
        id=id,
        clip_id=clip_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    id: str,
    clip_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[Union[DeleteDatasetClipResponse200, Error]]:
    """Delete a clip and its stored video. The dataset also goes with the watch and with the account.

    Args:
        id (str):
        clip_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DeleteDatasetClipResponse200, Error]]
    """

    kwargs = _get_kwargs(
        id=id,
        clip_id=clip_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    id: str,
    clip_id: str,
    *,
    client: AuthenticatedClient,
) -> Optional[Union[DeleteDatasetClipResponse200, Error]]:
    """Delete a clip and its stored video. The dataset also goes with the watch and with the account.

    Args:
        id (str):
        clip_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DeleteDatasetClipResponse200, Error]
    """

    return (
        await asyncio_detailed(
            id=id,
            clip_id=clip_id,
            client=client,
        )
    ).parsed
