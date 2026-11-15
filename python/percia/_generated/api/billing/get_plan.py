from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.get_plan_response_200 import GetPlanResponse200
from ...types import Response


def _get_kwargs() -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/plan",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Error, GetPlanResponse200]]:
    if response.status_code == 200:
        response_200 = GetPlanResponse200.from_dict(response.json())

        return response_200

    if response.status_code == 401:
        response_401 = Error.from_dict(response.json())

        return response_401

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Error, GetPlanResponse200]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
) -> Response[Union[Error, GetPlanResponse200]]:
    """Your plan (free, or pro shown as Pay as you go), its limits and your current counts. Limits count
    active watches only and bind only when `enforced` is true; when it is false they are just reported,
    so never ask the user to pause or delete anything because of them. `selling` says whether paid plans
    are on sale (false during the free preview). Pricing: $0.50 per camera-hour per camera (`pricing`),
    up to 10 active watches per camera (always enforced); `freeMinutesLeft` of the free camera-minutes,
    `monthToDate` camera-minutes and cost in cents, the spend cap `capCents`; watches pause for billing
    only when `billingEnforced` is true.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, GetPlanResponse200]]
    """

    kwargs = _get_kwargs()

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
) -> Optional[Union[Error, GetPlanResponse200]]:
    """Your plan (free, or pro shown as Pay as you go), its limits and your current counts. Limits count
    active watches only and bind only when `enforced` is true; when it is false they are just reported,
    so never ask the user to pause or delete anything because of them. `selling` says whether paid plans
    are on sale (false during the free preview). Pricing: $0.50 per camera-hour per camera (`pricing`),
    up to 10 active watches per camera (always enforced); `freeMinutesLeft` of the free camera-minutes,
    `monthToDate` camera-minutes and cost in cents, the spend cap `capCents`; watches pause for billing
    only when `billingEnforced` is true.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, GetPlanResponse200]
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
) -> Response[Union[Error, GetPlanResponse200]]:
    """Your plan (free, or pro shown as Pay as you go), its limits and your current counts. Limits count
    active watches only and bind only when `enforced` is true; when it is false they are just reported,
    so never ask the user to pause or delete anything because of them. `selling` says whether paid plans
    are on sale (false during the free preview). Pricing: $0.50 per camera-hour per camera (`pricing`),
    up to 10 active watches per camera (always enforced); `freeMinutesLeft` of the free camera-minutes,
    `monthToDate` camera-minutes and cost in cents, the spend cap `capCents`; watches pause for billing
    only when `billingEnforced` is true.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, GetPlanResponse200]]
    """

    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
) -> Optional[Union[Error, GetPlanResponse200]]:
    """Your plan (free, or pro shown as Pay as you go), its limits and your current counts. Limits count
    active watches only and bind only when `enforced` is true; when it is false they are just reported,
    so never ask the user to pause or delete anything because of them. `selling` says whether paid plans
    are on sale (false during the free preview). Pricing: $0.50 per camera-hour per camera (`pricing`),
    up to 10 active watches per camera (always enforced); `freeMinutesLeft` of the free camera-minutes,
    `monthToDate` camera-minutes and cost in cents, the spend cap `capCents`; watches pause for billing
    only when `billingEnforced` is true.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, GetPlanResponse200]
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
