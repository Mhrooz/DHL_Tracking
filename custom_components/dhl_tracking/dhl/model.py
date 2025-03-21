import json
import requests

from .dhl_event import DhlEvent
from .dhl_details import DhlDetails


URL = "https://api-eu.dhl.com/track/shipments"
API_KEY = "8CHuz4BNB6IBRyD75wpvgJ8yx6KfiomA"

TEST_TRACKING_NUMBER = "00340434498944707831"

# curl  -X GET 'https://api-eu.dhl.com/track/shipments?trackingNumber=00340434781076423558'
#       -H 'DHL-API-Key:8CHuz4BNB6IBRyD75wpvgJ8yx6KfiomA'

TEST_RESPONSE = """{}"""
try:
    with open("test_response.json", "r", encoding="utf-8") as file:
        TEST_RESPONSE = file.read()
except FileNotFoundError:
    print("File not found")


class DhlRequest:
    def __init__(self, tracking_numbers):
        self.tracking_numbers = tracking_numbers
        # self.json_info = self.get_tracking_info(tracking_numbers)
        TESTRESPONSEJSON = json.loads(TEST_RESPONSE)
        self.json_info = TESTRESPONSEJSON

        self.info = DhlInfo(self.json_info)

    def get_tracking_info(self, tracking_number):
        headers = {"DHL-API-Key": API_KEY}
        params = {"trackingNumber": tracking_number}
        response = requests.get(URL, headers=headers, params=params)
        return response.json()


class DhlInfo:
    """
    Class to get information about a DHL shipment
    """

    def __init__(self, json_info):
        self.info = json_info
        self.status = self.get_status()
        self.details = DhlDetails(self.info["shipments"][0]["details"])
        self.events = self.get_all_events()
        self.estimated_time_of_delivery = self.get_estimated_time_of_delivery()

    def get_tracking_info(self, tracking_number):
        headers = {"DHL-API-Key": API_KEY}
        params = {"trackingNumber": tracking_number}
        response = requests.get(URL, headers=headers, params=params)
        return response.json()

    def get_status(self):
        """
        Returns the current status of the shipment
        """
        return DhlEvent(self.info["shipments"][0]["status"])

    def get_weight(self):
        """
        Returns the weight of the shipment
        """
        return self.details.get_weight()

    def get_dimensions(self):
        """
        Returns the dimensions of the shipment
        """
        return self.details.get_dimensions()

    def get_product_name(self):
        """
        Returns the name of the product
        """
        return self.details.get_product_name()

    def get_estimated_time_of_delivery(self):
        """
        Returns the estimated time of estimated
        """
        return self.info["shipments"][0]["estimatedTimeOfDelivery"]

    def get_service_url(self):
        return self.info["shipments"][0]["serviceUrl"]

    def get_all_info(self):
        return self.info

    def get_all_events(self):
        events_json = self.info["shipments"][0]["events"]
        events_list = []
        for event in events_json:
            events_list.append(DhlEvent(event))
        return events_list


if __name__ == "__main__":
    dhl_info = DhlInfo(TEST_TRACKING_NUMBER)
    print("status: ", dhl_info.get_status())
    print("All events:")
    for event in dhl_info.get_all_events():
        print(event)
