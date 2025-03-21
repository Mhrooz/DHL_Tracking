class DhlEvent:
    def __init__(self, event):
        self.timestamp = event["timestamp"]
        self.status_code = event["statusCode"]
        self.status = event["status"]
        self.status_detailed = event["statusDetailed"]
        self.description = event["description"]
        self.remark = event["remark"]

    def get_timestamp(self):
        return self.timestamp

    def get_status_code(self):
        return self.status_code

    def get_status(self):
        return self.status

    def get_status_detailed(self):
        return self.status_detailed

    def get_description(self):
        return self.description

    def get_remark(self):
        return self.remark

    def __str__(self):
        return f"""
            Timestamp: {self.timestamp},
            Status: {self.status},
            Description: {self.description}
        """
