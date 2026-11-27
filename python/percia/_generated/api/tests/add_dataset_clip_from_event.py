from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.add_dataset_clip_from_event_body import AddDatasetClipFromEventBody
from ...models.add_dataset_clip_from_event_response_200 import (
    AddDatasetClipFromEventResponse200,
)
from ...models.add_dataset_clip_from_event_response_201 import (
    AddDatasetClipFromEventResponse201,
)
from ...models.error import Error
from ...types import Response


def _get_kwargs(
    id: str,
    *,
    body: AddDatasetClipFromEventBody,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/watches/{id}/dataset/from-event".format(
            id=id,
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[AddDatasetClipFromEventResponse200, AddDatasetClipFromEventResponse201, Error]]:
    if response.status_code == 200:
        response_200 = AddDatasetClipFromEventResponse200.from_dict(response.json())

        return response_200

    if response.status_code == 201:
        response_201 = AddDatasetClipFromEventResponse201.from_dict(response.json())

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

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[AddDatasetClipFromEventResponse200, AddDatasetClipFromEventResponse201, Error]]:
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
    body: AddDatasetClipFromEventBody,
) -> Response[Union[AddDatasetClipFromEventResponse200, AddDatasetClipFromEventResponse201, Error]]:
    """Keep an event's clip in the dataset with a label. An event already in the dataset only has its label
    changed. Marking an event Correct or False alarm does this by itself (should_match / should_not).

    Args:
        id (str):
        body (AddDatasetClipFromEventBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[AddDatasetClipFromEventResponse200, AddDatasetClipFromEventResponse201, Error]]
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
    body: AddDatasetClipFromEventBody,
) -> Optional[Union[AddDatasetClipFromEventResponse200, AddDatasetClipFromEventResponse201, Error]]:
    """Keep an event's clip in the dataset with a label. An event already in the dataset only has its label
    changed. Marking an event Correct or False alarm does this by itself (should_match / should_not).

    Args:
        id (str):
        body (AddDatasetClipFromEventBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[AddDatasetClipFromEventResponse200, AddDatasetClipFromEventResponse201, Error]
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
    body: AddDatasetClipFromEventBody,
) -> Response[Union[AddDatasetClipFromEventResponse200, AddDatasetClipFromEventResponse201, Error]]:
    """Keep an event's clip in the dataset with a label. An event already in the dataset only has its label
    changed. Marking an event Correct or False alarm does this by itself (should_match / should_not).

    Args:
        id (str):
        body (AddDatasetClipFromEventBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[AddDatasetClipFromEventResponse200, AddDatasetClipFromEventResponse201, Error]]
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
    body: AddDatasetClipFromEventBody,
) -> Optional[Union[AddDatasetClipFromEventResponse200, AddDatasetClipFromEventResponse201, Error]]:
    """Keep an event's clip in the dataset with a label. An event already in the dataset only has its label
    changed. Marking an event Correct or False alarm does this by itself (should_match / should_not).

    Args:
        id (str):
        body (AddDatasetClipFromEventBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[AddDatasetClipFromEventResponse200, AddDatasetClipFromEventResponse201, Error]
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
            body=body,
        )
    ).parsed
