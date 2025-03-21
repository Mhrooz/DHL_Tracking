"""Custom types for dhl_tracking."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.loader import Integration

    from .api import DhlTrackingApiClient
    from .coordinator import BlueprintDataUpdateCoordinator


type DhlTrackingConfigEntry = ConfigEntry[DhlTrackingData]


@dataclass
class DhlTrackingData:
    """Data for the Blueprint integration."""

    client: DhlTrackingApiClient
    coordinator: BlueprintDataUpdateCoordinator
    integration: Integration
