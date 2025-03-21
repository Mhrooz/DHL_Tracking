"""Adds config flow for Blueprint."""

from __future__ import annotations

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_API_TOKEN
from homeassistant.helpers import selector
from homeassistant.helpers.aiohttp_client import async_create_clientsession
from slugify import slugify

from .api import (
    DhlTrackingApiClient,
    DhlTrackingApiClientAuthenticationError,
    DhlTrackingApiClientCommunicationError,
    DhlTrackingApiClientError,
)
from .const import CONF_PACKET_NAME, CONF_TRACKING_NUMBER, DOMAIN, LOGGER


class BlueprintFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for Blueprint."""

    VERSION = 1

    async def async_step_user(
        self,
        user_input: dict | None = None,
    ) -> config_entries.ConfigFlowResult:
        """Handle a flow initialized by the user."""
        _errors = {}
        if user_input is not None:
            try:
                await self._test_credentials(
                    _api_token=user_input[CONF_API_TOKEN],
                    _tracking_number=user_input[CONF_TRACKING_NUMBER],
                    _packet_name=user_input[CONF_PACKET_NAME],
                )
            except DhlTrackingApiClientAuthenticationError as exception:
                LOGGER.warning(exception)
                _errors["base"] = "auth"
            except DhlTrackingApiClientCommunicationError as exception:
                LOGGER.error(exception)
                _errors["base"] = "connection"
            except DhlTrackingApiClientError as exception:
                LOGGER.exception(exception)
                _errors["base"] = "unknown"
            else:
                await self.async_set_unique_id(
                    ## Do NOT use this in production code
                    ## The unique_id should never be something that can change
                    ## https://developers.home-assistant.io/docs/config_entries_config_flow_handler#unique-ids
                    unique_id=slugify(user_input[CONF_TRACKING_NUMBER])
                )
                self._abort_if_unique_id_configured()
                return self.async_create_entry(
                    title=user_input[CONF_PACKET_NAME],
                    data=user_input,
                )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_API_TOKEN,
                        default=(user_input or {}).get(CONF_API_TOKEN, vol.UNDEFINED),
                    ): selector.TextSelector(
                        selector.TextSelectorConfig(
                            type=selector.TextSelectorType.TEXT,
                        ),
                    ),
                    vol.Required(
                        CONF_TRACKING_NUMBER,
                        default=(user_input or {}).get(
                            CONF_TRACKING_NUMBER, vol.UNDEFINED
                        ),
                    ): selector.TextSelector(
                        selector.TextSelectorConfig(
                            type=selector.TextSelectorType.TEXT,
                        ),
                    ),
                    vol.Required(
                        CONF_PACKET_NAME,
                        default=(user_input or {}).get(CONF_PACKET_NAME, vol.UNDEFINED),
                    ): selector.TextSelector(
                        selector.TextSelectorConfig(
                            type=selector.TextSelectorType.TEXT,
                        ),
                    ),
                },
            ),
            errors=_errors,
        )

    async def _test_credentials(
        self, _api_token: str, _tracking_number: str, _packet_name: str
    ) -> None:
        """Validate credentials."""
        client = DhlTrackingApiClient(
            _api_token=_api_token,
            _tracking_number=_tracking_number,
            _packet_name=_packet_name,
            session=async_create_clientsession(self.hass),
        )
        await client.async_get_data()
