from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.set_billing_cap_body import SetBillingCapBody
from ...models.set_billing_cap_response_200 import SetBillingCapResponse200
from ...types import Response


def _get_kwargs(
    *,
    body: SetBillingCapBody,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": "/billing/cap",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Error, SetBillingCapResponse200]]:
    if response.status_code == 200:
        response_200 = SetBillingCapResponse200.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = Error.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = Error.from_dict(response.json())

        return response_401

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Error, SetBillingCapResponse200]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: SetBillingCapBody,
) -> Response[Union[Error, SetBillingCapResponse200]]:
    """Set your monthly spend cap in cents ($5 to $10,000; default $200). When this month's camera time
    reaches it, watches pause (only while billing is enforced). Change it only when the person asks.

    Args:
        body (SetBillingCapBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, SetBillingCapResponse200]]
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
    body: SetBillingCapBody,
) -> Optional[Union[Error, SetBillingCapResponse200]]:
    """Set your monthly spend cap in cents ($5 to $10,000; default $200). When this month's camera time
    reaches it, watches pause (only while billing is enforced). Change it only when the person asks.

    Args:
        body (SetBillingCapBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, SetBillingCapResponse200]
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: SetBillingCapBody,
) -> Response[Union[Error, SetBillingCapResponse200]]:
    """Set your monthly spend cap in cents ($5 to $10,000; default $200). When this month's camera time
    reaches it, watches pause (only while billing is enforced). Change it only when the person asks.

    Args:
        body (SetBillingCapBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, SetBillingCapResponse200]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: SetBillingCapBody,
) -> Optional[Union[Error, SetBillingCapResponse200]]:
    """Set your monthly spend cap in cents ($5 to $10,000; default $200). When this month's camera time
    reaches it, watches pause (only while billing is enforced). Change it only when the person asks.

    Args:
        body (SetBillingCapBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, SetBillingCapResponse200]
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
