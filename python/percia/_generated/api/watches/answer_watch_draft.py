from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.answer_watch_draft_body import AnswerWatchDraftBody
from ...models.answer_watch_draft_response_200 import AnswerWatchDraftResponse200
from ...models.error import Error
from ...types import Response


def _get_kwargs(
    id: str,
    *,
    body: AnswerWatchDraftBody,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/watches/draft/{id}/answer".format(
            id=id,
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[AnswerWatchDraftResponse200, Error]]:
    if response.status_code == 200:
        response_200 = AnswerWatchDraftResponse200.from_dict(response.json())

        return response_200

    if response.status_code == 402:
        response_402 = Error.from_dict(response.json())

        return response_402

    if response.status_code == 404:
        response_404 = Error.from_dict(response.json())

        return response_404

    if response.status_code == 409:
        response_409 = Error.from_dict(response.json())

        return response_409

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
) -> Response[Union[AnswerWatchDraftResponse200, Error]]:
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
    body: AnswerWatchDraftBody,
) -> Response[Union[AnswerWatchDraftResponse200, Error]]:
    r"""Answer the draft's question: `text` is the number of one of the options (\"2\") or the person's own
    words. Only a draft that is still clarifying takes an answer; a draft that became a watch is closed
    (a running watch is never questioned). Returns the updated draft (a new question, or ready). When
    the layer cannot use the words, they are joined to the first ask and read again as one new ask
    (`restated: true`).

    Args:
        id (str):
        body (AnswerWatchDraftBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[AnswerWatchDraftResponse200, Error]]
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
    body: AnswerWatchDraftBody,
) -> Optional[Union[AnswerWatchDraftResponse200, Error]]:
    r"""Answer the draft's question: `text` is the number of one of the options (\"2\") or the person's own
    words. Only a draft that is still clarifying takes an answer; a draft that became a watch is closed
    (a running watch is never questioned). Returns the updated draft (a new question, or ready). When
    the layer cannot use the words, they are joined to the first ask and read again as one new ask
    (`restated: true`).

    Args:
        id (str):
        body (AnswerWatchDraftBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[AnswerWatchDraftResponse200, Error]
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
    body: AnswerWatchDraftBody,
) -> Response[Union[AnswerWatchDraftResponse200, Error]]:
    r"""Answer the draft's question: `text` is the number of one of the options (\"2\") or the person's own
    words. Only a draft that is still clarifying takes an answer; a draft that became a watch is closed
    (a running watch is never questioned). Returns the updated draft (a new question, or ready). When
    the layer cannot use the words, they are joined to the first ask and read again as one new ask
    (`restated: true`).

    Args:
        id (str):
        body (AnswerWatchDraftBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[AnswerWatchDraftResponse200, Error]]
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
    body: AnswerWatchDraftBody,
) -> Optional[Union[AnswerWatchDraftResponse200, Error]]:
    r"""Answer the draft's question: `text` is the number of one of the options (\"2\") or the person's own
    words. Only a draft that is still clarifying takes an answer; a draft that became a watch is closed
    (a running watch is never questioned). Returns the updated draft (a new question, or ready). When
    the layer cannot use the words, they are joined to the first ask and read again as one new ask
    (`restated: true`).

    Args:
        id (str):
        body (AnswerWatchDraftBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[AnswerWatchDraftResponse200, Error]
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
            body=body,
        )
    ).parsed
