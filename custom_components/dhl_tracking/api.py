"""Sample API Client."""

from __future__ import annotations

import json
import socket
from typing import Any

import aiohttp
import async_timeout

from .dhl.model import DhlInfo


class DhlTrackingApiClientError(Exception):
    """Exception to indicate a general API error."""


class DhlTrackingApiClientCommunicationError(
    DhlTrackingApiClientError,
):
    """Exception to indicate a communication error."""


class DhlTrackingApiClientAuthenticationError(
    DhlTrackingApiClientError,
):
    """Exception to indicate an authentication error."""


def _verify_response_or_raise(response: aiohttp.ClientResponse) -> None:
    """Verify that the response is valid."""
    if response.status in (401, 403):
        msg = "Invalid credentials"
        raise DhlTrackingApiClientAuthenticationError(
            msg,
        )
    response.raise_for_status()


# class DhlTrackingApiClient
class DhlTrackingApiClient:
    """Sample API Client."""

    def __init__(
        self,
        _api_token: str,
        _tracking_number: str,
        session: aiohttp.ClientSession,
    ) -> None:
        """Sample API Client."""
        self._api_token = _api_token
        self._tracking_number = _tracking_number
        self._session = session

    async def async_get_data(self) -> Any:
        """Get data from the API."""
        """
        return await self._api_wrapper(
            method="get",
            url="https://jsonplaceholder.typicode.com/posts/1",
        )
        """
        json_info = await self._api_wrapper(
            method="get",
            url=f"https://api-eu.dhl.com/track/shipments?trackingNumber={self._tracking_number}",
            headers={"DHL-API-Key": self._api_token},
        )
        return DhlInfo(json_info=json.loads(json_info))

    async def async_set_title(self, value: str) -> Any:
        """Get data from the API."""
        return await self._api_wrapper(
            method="patch",
            url="https://jsonplaceholder.typicode.com/posts/1",
            data={"title": value},
            headers={"Content-type": "application/json; charset=UTF-8"},
        )

    async def _api_wrapper(
        self,
        method: str,
        url: str,
        data: dict | None = None,
        headers: dict | None = None,
    ) -> Any:
        """Get information from the API."""
        try:
            async with async_timeout.timeout(10):
                response = await self._session.request(
                    method=method,
                    url=url,
                    headers=headers,
                    json=data,
                )
                _verify_response_or_raise(response)
                return await response.json()

        except TimeoutError as exception:
            msg = f"Timeout error fetching information - {exception}"
            raise DhlTrackingApiClientCommunicationError(
                msg,
            ) from exception
        except (aiohttp.ClientError, socket.gaierror) as exception:
            msg = f"Error fetching information - {exception}"
            raise DhlTrackingApiClientCommunicationError(
                msg,
            ) from exception
        except Exception as exception:  # pylint: disable=broad-except
            msg = f"Something really wrong happened! - {exception}"
            raise DhlTrackingApiClientError(
                msg,
            ) from exception
