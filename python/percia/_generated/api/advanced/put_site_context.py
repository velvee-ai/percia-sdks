from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.put_site_context_body import PutSiteContextBody
from ...models.put_site_context_response_200 import PutSiteContextResponse200
from ...types import Response


def _get_kwargs(
    id: str,
    *,
    body: PutSiteContextBody,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/sites/{id}/context".format(
            id=id,
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Error, PutSiteContextResponse200]]:
    if response.status_code == 200:
        response_200 = PutSiteContextResponse200.from_dict(response.json())

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

    if response.status_code == 403:
        response_403 = Error.from_dict(response.json())

        return response_403

    if response.status_code == 404:
        response_404 = Error.from_dict(response.json())

        return response_404

    if response.status_code == 412:
        response_412 = Error.from_dict(response.json())

        return response_412

    if response.status_code == 413:
        response_413 = Error.from_dict(response.json())

        return response_413

    if response.status_code == 422:
        response_422 = Error.from_dict(response.json())

        return response_422

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Error, PutSiteContextResponse200]]:
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
    body: PutSiteContextBody,
) -> Response[Union[Error, PutSiteContextResponse200]]:
    """Replace the site's context (SiteContext): calibration, facts, zones, signal declarations (advanced)

     where recording is on only. Replace the SiteContext of a site you own : `context` (scene, subjects,
    notes), `facts`, `cameras[]` (mount, calibration, registration), `zones`, `reference_images`, and
    `signals[]`, the declarations of the machine channels you will POST to /signals (name, kind, unit,
    nominal and worst_case_rate_hz, clock_offset_s, lag_s, latency_s, each timing with its uncertainty).
    Leave out tenant_id, site_id, revision and updated_at: the server sets them. Send `If-Match:
    <revision>` to avoid overwriting a newer write. A changed document bumps `revision`, and the site's
    running advanced watches re-plan on it without a restart. Free text in a context is customer data
    and is shown to models as background, never as instructions. Needs scope context:write.

    Args:
        id (str):
        body (PutSiteContextBody): A SiteContext without tenant_id, site_id, revision, updated_at:
            `context {scene, subjects, notes}`, `facts[]`, `cameras[]`, `zones[]`,
            `reference_images[]`, `signals[]` (declarations). See /docs/advanced.md.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, PutSiteContextResponse200]]
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
    body: PutSiteContextBody,
) -> Optional[Union[Error, PutSiteContextResponse200]]:
    """Replace the site's context (SiteContext): calibration, facts, zones, signal declarations (advanced)

     where recording is on only. Replace the SiteContext of a site you own : `context` (scene, subjects,
    notes), `facts`, `cameras[]` (mount, calibration, registration), `zones`, `reference_images`, and
    `signals[]`, the declarations of the machine channels you will POST to /signals (name, kind, unit,
    nominal and worst_case_rate_hz, clock_offset_s, lag_s, latency_s, each timing with its uncertainty).
    Leave out tenant_id, site_id, revision and updated_at: the server sets them. Send `If-Match:
    <revision>` to avoid overwriting a newer write. A changed document bumps `revision`, and the site's
    running advanced watches re-plan on it without a restart. Free text in a context is customer data
    and is shown to models as background, never as instructions. Needs scope context:write.

    Args:
        id (str):
        body (PutSiteContextBody): A SiteContext without tenant_id, site_id, revision, updated_at:
            `context {scene, subjects, notes}`, `facts[]`, `cameras[]`, `zones[]`,
            `reference_images[]`, `signals[]` (declarations). See /docs/advanced.md.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, PutSiteContextResponse200]
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
    body: PutSiteContextBody,
) -> Response[Union[Error, PutSiteContextResponse200]]:
    """Replace the site's context (SiteContext): calibration, facts, zones, signal declarations (advanced)

     where recording is on only. Replace the SiteContext of a site you own : `context` (scene, subjects,
    notes), `facts`, `cameras[]` (mount, calibration, registration), `zones`, `reference_images`, and
    `signals[]`, the declarations of the machine channels you will POST to /signals (name, kind, unit,
    nominal and worst_case_rate_hz, clock_offset_s, lag_s, latency_s, each timing with its uncertainty).
    Leave out tenant_id, site_id, revision and updated_at: the server sets them. Send `If-Match:
    <revision>` to avoid overwriting a newer write. A changed document bumps `revision`, and the site's
    running advanced watches re-plan on it without a restart. Free text in a context is customer data
    and is shown to models as background, never as instructions. Needs scope context:write.

    Args:
        id (str):
        body (PutSiteContextBody): A SiteContext without tenant_id, site_id, revision, updated_at:
            `context {scene, subjects, notes}`, `facts[]`, `cameras[]`, `zones[]`,
            `reference_images[]`, `signals[]` (declarations). See /docs/advanced.md.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, PutSiteContextResponse200]]
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
    body: PutSiteContextBody,
) -> Optional[Union[Error, PutSiteContextResponse200]]:
    """Replace the site's context (SiteContext): calibration, facts, zones, signal declarations (advanced)

     where recording is on only. Replace the SiteContext of a site you own : `context` (scene, subjects,
    notes), `facts`, `cameras[]` (mount, calibration, registration), `zones`, `reference_images`, and
    `signals[]`, the declarations of the machine channels you will POST to /signals (name, kind, unit,
    nominal and worst_case_rate_hz, clock_offset_s, lag_s, latency_s, each timing with its uncertainty).
    Leave out tenant_id, site_id, revision and updated_at: the server sets them. Send `If-Match:
    <revision>` to avoid overwriting a newer write. A changed document bumps `revision`, and the site's
    running advanced watches re-plan on it without a restart. Free text in a context is customer data
    and is shown to models as background, never as instructions. Needs scope context:write.

    Args:
        id (str):
        body (PutSiteContextBody): A SiteContext without tenant_id, site_id, revision, updated_at:
            `context {scene, subjects, notes}`, `facts[]`, `cameras[]`, `zones[]`,
            `reference_images[]`, `signals[]` (declarations). See /docs/advanced.md.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, PutSiteContextResponse200]
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
            body=body,
        )
    ).parsed
