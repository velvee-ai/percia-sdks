from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.redeem_credit_code_body import RedeemCreditCodeBody
from ...models.redeem_credit_code_response_200 import RedeemCreditCodeResponse200
from ...types import Response


def _get_kwargs(
    *,
    body: RedeemCreditCodeBody,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/billing/redeem",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Error, RedeemCreditCodeResponse200]]:
    if response.status_code == 200:
        response_200 = RedeemCreditCodeResponse200.from_dict(response.json())

        return response_200

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

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Error, RedeemCreditCodeResponse200]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: RedeemCreditCodeBody,
) -> Response[Union[Error, RedeemCreditCodeResponse200]]:
    """Redeem a credit code for camera-minutes (credits are minutes of watching, used before the free
    minutes and before the card). A code is shown to its owner once: pass it in the body, never in a
    URL. Needs a card on file while billing is on sale: without one it answers 402 card_required with
    addCardUrl (the Billing page; only a person can add a card) and the code is not checked or used.
    Unknown, disabled and expired codes all answer 404 code_invalid; a code with no redemption left is
    409 code_fully_claimed; the same person redeeming twice is 409 code_already_redeemed; too many tries
    is 429 rate_limited with Retry-After.

    Args:
        body (RedeemCreditCodeBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, RedeemCreditCodeResponse200]]
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
    body: RedeemCreditCodeBody,
) -> Optional[Union[Error, RedeemCreditCodeResponse200]]:
    """Redeem a credit code for camera-minutes (credits are minutes of watching, used before the free
    minutes and before the card). A code is shown to its owner once: pass it in the body, never in a
    URL. Needs a card on file while billing is on sale: without one it answers 402 card_required with
    addCardUrl (the Billing page; only a person can add a card) and the code is not checked or used.
    Unknown, disabled and expired codes all answer 404 code_invalid; a code with no redemption left is
    409 code_fully_claimed; the same person redeeming twice is 409 code_already_redeemed; too many tries
    is 429 rate_limited with Retry-After.

    Args:
        body (RedeemCreditCodeBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, RedeemCreditCodeResponse200]
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: RedeemCreditCodeBody,
) -> Response[Union[Error, RedeemCreditCodeResponse200]]:
    """Redeem a credit code for camera-minutes (credits are minutes of watching, used before the free
    minutes and before the card). A code is shown to its owner once: pass it in the body, never in a
    URL. Needs a card on file while billing is on sale: without one it answers 402 card_required with
    addCardUrl (the Billing page; only a person can add a card) and the code is not checked or used.
    Unknown, disabled and expired codes all answer 404 code_invalid; a code with no redemption left is
    409 code_fully_claimed; the same person redeeming twice is 409 code_already_redeemed; too many tries
    is 429 rate_limited with Retry-After.

    Args:
        body (RedeemCreditCodeBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, RedeemCreditCodeResponse200]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: RedeemCreditCodeBody,
) -> Optional[Union[Error, RedeemCreditCodeResponse200]]:
    """Redeem a credit code for camera-minutes (credits are minutes of watching, used before the free
    minutes and before the card). A code is shown to its owner once: pass it in the body, never in a
    URL. Needs a card on file while billing is on sale: without one it answers 402 card_required with
    addCardUrl (the Billing page; only a person can add a card) and the code is not checked or used.
    Unknown, disabled and expired codes all answer 404 code_invalid; a code with no redemption left is
    409 code_fully_claimed; the same person redeeming twice is 409 code_already_redeemed; too many tries
    is 429 rate_limited with Retry-After.

    Args:
        body (RedeemCreditCodeBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, RedeemCreditCodeResponse200]
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
