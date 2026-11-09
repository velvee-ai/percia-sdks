from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.send_event_feedback_body import SendEventFeedbackBody
from ...models.send_event_feedback_response_200 import SendEventFeedbackResponse200
from ...types import Response


def _get_kwargs(
    id: str,
    event_id: str,
    *,
    body: SendEventFeedbackBody,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/watches/{id}/events/{event_id}/feedback".format(
            id=id,
            event_id=event_id,
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Error, SendEventFeedbackResponse200]]:
    if response.status_code == 200:
        response_200 = SendEventFeedbackResponse200.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = Error.from_dict(response.json())

        return response_400

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
) -> Response[Union[Error, SendEventFeedbackResponse200]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: str,
    event_id: str,
    *,
    client: AuthenticatedClient,
    body: SendEventFeedbackBody,
) -> Response[Union[Error, SendEventFeedbackResponse200]]:
    """Mark an event correct or a false alarm. With a keyframe it becomes (or updates) a test case with the
    image pinned.

    Args:
        id (str):
        event_id (str):
        body (SendEventFeedbackBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, SendEventFeedbackResponse200]]
    """

    kwargs = _get_kwargs(
        id=id,
        event_id=event_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    id: str,
    event_id: str,
    *,
    client: AuthenticatedClient,
    body: SendEventFeedbackBody,
) -> Optional[Union[Error, SendEventFeedbackResponse200]]:
    """Mark an event correct or a false alarm. With a keyframe it becomes (or updates) a test case with the
    image pinned.

    Args:
        id (str):
        event_id (str):
        body (SendEventFeedbackBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, SendEventFeedbackResponse200]
    """

    return sync_detailed(
        id=id,
        event_id=event_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    id: str,
    event_id: str,
    *,
    client: AuthenticatedClient,
    body: SendEventFeedbackBody,
) -> Response[Union[Error, SendEventFeedbackResponse200]]:
    """Mark an event correct or a false alarm. With a keyframe it becomes (or updates) a test case with the
    image pinned.

    Args:
        id (str):
        event_id (str):
        body (SendEventFeedbackBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, SendEventFeedbackResponse200]]
    """

    kwargs = _get_kwargs(
        id=id,
        event_id=event_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    id: str,
    event_id: str,
    *,
    client: AuthenticatedClient,
    body: SendEventFeedbackBody,
) -> Optional[Union[Error, SendEventFeedbackResponse200]]:
    """Mark an event correct or a false alarm. With a keyframe it becomes (or updates) a test case with the
    image pinned.

    Args:
        id (str):
        event_id (str):
        body (SendEventFeedbackBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, SendEventFeedbackResponse200]
    """

    return (
        await asyncio_detailed(
            id=id,
            event_id=event_id,
            client=client,
            body=body,
        )
    ).parsed
