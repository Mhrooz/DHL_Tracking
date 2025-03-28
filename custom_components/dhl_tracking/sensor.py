"""Sensor platform for dhl_tracking."""

from __future__ import annotations  # noqa: I001

from typing import TYPE_CHECKING

from homeassistant.components.sensor import SensorEntity, SensorEntityDescription

from .entity import DhlTrackingEntity


if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

    from .coordinator import BlueprintDataUpdateCoordinator
    from .data import DhlTrackingConfigEntry

ENTITY_DESCRIPTIONS = (
    SensorEntityDescription(
        key="dhl_tracking",
        name="Packet Name",
        icon="mdi:format-quote-close",
    ),
)

DHL_ESTIMATE_TIME_ENTITY_DESCRIPTIONS = (
    SensorEntityDescription(
        key="dhl_estimate_time",
        name="Packet ETA",
        icon="mdi:timer",
    ),
)

DHL_CURRENT_STATUS_ENTITY_DESCRIPTIONS = (
    SensorEntityDescription(
        key="dhl_current_status",
        name="Packet Status",
        icon="mdi:package-variant-closed",
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001 Unused function argument: `hass`
    entry: DhlTrackingConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""
    async_add_entities(
        DhlTrackingSensor(
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
    async_add_entities(
        DhlCurrentStatusSensor(
            coordinator=entry.runtime_data.coordinator,
            entity_description=entity_description,
        )
        for entity_description in DHL_CURRENT_STATUS_ENTITY_DESCRIPTIONS
    )


class DhlTrackingSensor(DhlTrackingEntity, SensorEntity):
    """integration_blueprint Sensor class."""

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


class DhlEstimateTimeSensor(DhlTrackingEntity, SensorEntity):
    """dhl_tracking Sensor class."""

    def __init__(
        self,
        coordinator: BlueprintDataUpdateCoordinator,
        entity_description: SensorEntityDescription,
    ) -> None:
        """Initialize the sensor class."""
        super().__init__(coordinator)
        self.entity_description = entity_description
        self.unique_id = coordinator.config_entry.entry_id + "_dhl_estimate_time"

    @property
    def native_value(self) -> str | None:
        """Return the native value of the sensor."""
        dhl_info = self.coordinator.data
        return dhl_info.get_estimated_time_of_delivery()


class DhlCurrentStatusSensor(DhlTrackingEntity, SensorEntity):
    """dhl_tracking Sensor class."""

    def __init__(
        self,
        coordinator: BlueprintDataUpdateCoordinator,
        entity_description: SensorEntityDescription,
    ) -> None:
        """Initialize the sensor class."""
        super().__init__(coordinator)
        self.entity_description = entity_description
        self.unique_id = coordinator.config_entry.entry_id + "current_status"

    @property
    def native_value(self) -> str | None:
        """Return the native value of the sensor."""
        dhl_info = self.coordinator.data
        return dhl_info.get_status().get_status_code()
