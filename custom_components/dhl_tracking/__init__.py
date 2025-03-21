"""
Custom integration to integrate dhl_tracking with Home Assistant.

For more details about this integration, please refer to
https://github.com/Mhrooz/dhl_tracking
"""

from __future__ import annotations

from datetime import timedelta
from typing import TYPE_CHECKING

from homeassistant.const import CONF_API_TOKEN, Platform
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.loader import async_get_loaded_integration

from .api import DhlTrackingApiClient
from .const import CONF_TRACKING_NUMBER, DOMAIN, LOGGER
from .coordinator import BlueprintDataUpdateCoordinator
from .data import DhlTrackingData

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant

    from .data import DhlTrackingConfigEntry

PLATFORMS: list[Platform] = [
    Platform.SENSOR,
]


# https://developers.home-assistant.io/docs/config_entries_index/#setting-up-an-entry
async def async_setup_entry(
    hass: HomeAssistant,
    entry: DhlTrackingConfigEntry,
) -> bool:
    """Set up this integration using UI."""
    coordinator = BlueprintDataUpdateCoordinator(
        hass=hass,
        logger=LOGGER,
        name=DOMAIN,
        update_interval=timedelta(hours=2),
    )

    entry.runtime_data = DhlTrackingData(
        client=DhlTrackingApiClient(
            _api_token=entry.data[CONF_API_TOKEN],
            _tracking_number=entry.data[CONF_TRACKING_NUMBER],
            session=async_get_clientsession(hass),
        ),
        integration=async_get_loaded_integration(hass, entry.domain),
        coordinator=coordinator,
    )

    # https://developers.home-assistant.io/docs/integration_fetching_data#coordinated-single-api-poll-for-data-for-all-entities
    await coordinator.async_config_entry_first_refresh()

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    entry.async_on_unload(entry.add_update_listener(async_reload_entry))

    return True


async def async_unload_entry(
    hass: HomeAssistant,
    entry: DhlTrackingConfigEntry,
) -> bool:
    """Handle removal of an entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)


async def async_reload_entry(
    hass: HomeAssistant,
    entry: DhlTrackingConfigEntry,
) -> None:
    """Reload config entry."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)
