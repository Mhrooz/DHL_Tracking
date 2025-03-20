"""Sensor platform for dhl_tracking."""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.components.sensor import SensorEntity, SensorEntityDescription

from .entity import IntegrationBlueprintEntity

from .dhl.model import DhlInfo

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

    from .coordinator import BlueprintDataUpdateCoordinator
    from .data import IntegrationBlueprintConfigEntry

ENTITY_DESCRIPTIONS = (
    SensorEntityDescription(
        key="dhl_tracking",
        name="Integration Sensor",
        icon="mdi:format-quote-close",
    ),
)

DHL_ESTIMATE_TIME_ENTITY_DESCRIPTIONS = (
    SensorEntityDescription(
        key="dhl_estimate_time",
        name="Package Arrival Time",
        icon="mdi:timer",
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001 Unused function argument: `hass`
    entry: IntegrationBlueprintConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""
    async_add_entities(
        IntegrationBlueprintSensor(
            coordinator=entry.runtime_data.coordinator,
            entity_description=entity_description,
        )
        for entity_description in ENTITY_DESCRIPTIONS
    )
    async_add_entities(
        DhlEstimateTimeSensor(
            coordinator=entry.runtime_data.coordinator,
            entity_description=entity_description,
        )
        for entity_description in DHL_ESTIMATE_TIME_ENTITY_DESCRIPTIONS
    )


class IntegrationBlueprintSensor(IntegrationBlueprintEntity, SensorEntity):
    """dhl_tracking Sensor class."""

    def __init__(
        self,
        coordinator: BlueprintDataUpdateCoordinator,
        entity_description: SensorEntityDescription,
    ) -> None:
        """Initialize the sensor class."""
        super().__init__(coordinator)
        self.entity_description = entity_description

    @property
    def native_value(self) -> str | None:
        """Return the native value of the sensor."""
        return self.coordinator.data.get_product_name()


class DhlEstimateTimeSensor(IntegrationBlueprintEntity, SensorEntity):
    """dhl_tracking Sensor class."""

    def __init__(
        self,
        coordinator: BlueprintDataUpdateCoordinator,
        entity_description: SensorEntityDescription,
    ) -> None:
        """Initialize the sensor class."""
        super().__init__(coordinator)
        self.entity_description = entity_description
        # TODO: Set unique_id to the tracking number
        self.unique_id = "914JDWXMAI0Z5GANQM"

    @property
    def native_value(self) -> str | None:
        """Return the native value of the sensor."""
        # return self.coordinator.data.get("title")
        dhl_info = self.coordinator.data
        return dhl_info.get_estimated_time_of_delivery()
