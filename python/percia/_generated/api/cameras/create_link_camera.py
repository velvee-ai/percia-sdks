from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_link_camera_body import CreateLinkCameraBody
from ...models.create_link_camera_response_200 import CreateLinkCameraResponse200
from ...models.create_link_camera_response_201 import CreateLinkCameraResponse201
from ...models.error import Error
from ...types import Response


def _get_kwargs(
    *,
    body: CreateLinkCameraBody,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/cameras/link",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[CreateLinkCameraResponse200, CreateLinkCameraResponse201, Error]]:
    if response.status_code == 200:
        response_200 = CreateLinkCameraResponse200.from_dict(response.json())

        return response_200

    if response.status_code == 201:
        response_201 = CreateLinkCameraResponse201.from_dict(response.json())

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

    if response.status_code == 429:
        response_429 = Error.from_dict(response.json())

        return response_429

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[CreateLinkCameraResponse200, CreateLinkCameraResponse201, Error]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: CreateLinkCameraBody,
) -> Response[Union[CreateLinkCameraResponse200, CreateLinkCameraResponse201, Error]]:
    """Make a camera from a public video link (rtsp, rtsps, http or https). Percia pulls it on its media
    host while a watch on it is active, so the camera then works like any other: use percia-cam://<id>
    as a watch's sourceUrl. The same link returns the same camera (200, existing true). A watch created
    with the link itself as sourceUrl does this for you. A private address (192.168.x.x, 10.x.x.x,
    localhost, an ONVIF/RTSP/Frigate/Home Assistant camera on a home network) is refused with 400 and a
    pointer to the Percia bridge. 404 unless link cameras are on.

    Args:
        body (CreateLinkCameraBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CreateLinkCameraResponse200, CreateLinkCameraResponse201, Error]]
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
    body: CreateLinkCameraBody,
) -> Optional[Union[CreateLinkCameraResponse200, CreateLinkCameraResponse201, Error]]:
    """Make a camera from a public video link (rtsp, rtsps, http or https). Percia pulls it on its media
    host while a watch on it is active, so the camera then works like any other: use percia-cam://<id>
    as a watch's sourceUrl. The same link returns the same camera (200, existing true). A watch created
    with the link itself as sourceUrl does this for you. A private address (192.168.x.x, 10.x.x.x,
    localhost, an ONVIF/RTSP/Frigate/Home Assistant camera on a home network) is refused with 400 and a
    pointer to the Percia bridge. 404 unless link cameras are on.

    Args:
        body (CreateLinkCameraBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CreateLinkCameraResponse200, CreateLinkCameraResponse201, Error]
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: CreateLinkCameraBody,
) -> Response[Union[CreateLinkCameraResponse200, CreateLinkCameraResponse201, Error]]:
    """Make a camera from a public video link (rtsp, rtsps, http or https). Percia pulls it on its media
    host while a watch on it is active, so the camera then works like any other: use percia-cam://<id>
    as a watch's sourceUrl. The same link returns the same camera (200, existing true). A watch created
    with the link itself as sourceUrl does this for you. A private address (192.168.x.x, 10.x.x.x,
    localhost, an ONVIF/RTSP/Frigate/Home Assistant camera on a home network) is refused with 400 and a
    pointer to the Percia bridge. 404 unless link cameras are on.

    Args:
        body (CreateLinkCameraBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CreateLinkCameraResponse200, CreateLinkCameraResponse201, Error]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: CreateLinkCameraBody,
) -> Optional[Union[CreateLinkCameraResponse200, CreateLinkCameraResponse201, Error]]:
    """Make a camera from a public video link (rtsp, rtsps, http or https). Percia pulls it on its media
    host while a watch on it is active, so the camera then works like any other: use percia-cam://<id>
    as a watch's sourceUrl. The same link returns the same camera (200, existing true). A watch created
    with the link itself as sourceUrl does this for you. A private address (192.168.x.x, 10.x.x.x,
    localhost, an ONVIF/RTSP/Frigate/Home Assistant camera on a home network) is refused with 400 and a
    pointer to the Percia bridge. 404 unless link cameras are on.

    Args:
        body (CreateLinkCameraBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CreateLinkCameraResponse200, CreateLinkCameraResponse201, Error]
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
