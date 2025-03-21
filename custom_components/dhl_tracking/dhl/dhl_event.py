class DhlEvent:
    """
    Represents an event in the DHL tracking system.

    This class encapsulates details about a specific event, including its timestamp,
    status, detailed status, description, and any additional remarks.
    """

    def __init__(self, event: dict) -> None:
        """
        Initialize a DhlEvent instance.

        Args:
            event (dict): A dictionary containing event details such as timestamp,
            status, and description.

        """
        self.timestamp = event["timestamp"]
        self.status_code = event["statusCode"]
        self.status = event["status"]
        self.status_detailed = event["statusDetailed"]
        self.description = event["description"]
        self.remark = event["remark"]

    def get_timestamp(self) -> str:
        """Return the timestamp of the event."""
        return self.timestamp

    def get_status_code(self) -> str:
        """Return the status code of the event."""
        return self.status_code

    def get_status(self) -> str:
        """Return the status of the event."""
        return self.status

    def get_status_detailed(self) -> str:
        """Return the detailed status of the event."""
        return self.status_detailed

    def get_description(self) -> str:
        """Return the description of the event."""
        return self.description

    def get_remark(self) -> str:
        """Return the remark of the event."""
        return self.remark

    def __str__(self) -> str:
        """
        Return a string representation of the DhlEvent instance.

        This includes the timestamp, status, and description of the event.
        """
        return f"""
            Timestamp: {self.timestamp},
            Status: {self.status},
            Description: {self.description}
        """
