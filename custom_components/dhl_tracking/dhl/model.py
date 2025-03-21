"""Provides the DhlInfo class for interacting with the DHL shipment tracking API."""

from .dhl_details import DhlDetails, DhlDimensions  # noqa: I001
from .dhl_event import DhlEvent

import requests


URL = "https://api-eu.dhl.com/track/shipments"
API_KEY = "8CHuz4BNB6IBRyD75wpvgJ8yx6KfiomA"

TEST_TRACKING_NUMBER = "00340434498944707831"


class DhlInfo:
    """Class to get information about a DHL shipment."""

    def __init__(self, json_info: dict) -> None:
        """
        Initialize the DhlInfo object with shipment information.

        Args:
            json_info (dict): The JSON information about the shipment.

        """
        self.info = json_info
        self.status = self.get_status()
        self.details = DhlDetails(self.info["shipments"][0]["details"])
        self.events = self.get_all_events()
        self.estimated_time_of_delivery = self.get_estimated_time_of_delivery()

    def get_tracking_info(self, tracking_number: str) -> dict:
        """
        Fetch tracking information for a given tracking number.

        Args:
            tracking_number (str): The tracking number of the shipment.

        Returns:
            dict: The tracking information as a dictionary.

        """
        headers = {"DHL-API-Key": API_KEY}
        params = {"trackingNumber": tracking_number}
        response = requests.get(URL, headers=headers, params=params, timeout=10)
        return response.json()

    def get_status(self) -> DhlEvent:
        """Return the current status of the shipment."""
        return DhlEvent(self.info["shipments"][0]["status"])

    def get_weight(self) -> float:
        """Return the weight of the shipment."""
        return self.details.get_weight()

    def get_dimensions(self) -> DhlDimensions | None:
        """Return the dimensions of the shipment."""
        return self.details.get_dimensions()

    def get_product_name(self) -> str:
        """Return the name of the product."""
        return self.details.get_product_name()

    def get_estimated_time_of_delivery(self) -> str | None:
        """Return the estimated time of delivery."""
        if self.get_status().get_status_code() == "delivered":
            return "Delivered"
        if "estimatedTimeOfDelivery" not in self.info["shipments"][0]:
            return "N/A"
        return self.info["shipments"][0]["estimatedTimeOfDelivery"]

    def get_service_url(self) -> str:
        """Return the service URL."""
        return self.info["shipments"][0]["serviceUrl"]

    def get_all_info(self) -> dict:
        """Return all the information about the shipment."""
        return self.info

    def get_all_events(self) -> list[DhlEvent]:
        """Return all the events of the shipment."""
        events_json = self.info["shipments"][0]["events"]
        return [DhlEvent(event) for event in events_json]


if __name__ == "__main__":
    pass
