"""
Module containing classes to represent DHL shipment details and dimensions.

Classes:
- DhlDimensions: Represents DHL package dimensions (length, width, height, and units).
- DhlDetails: Represents DHL shipment details (product name, weight, and dimensions).
"""


class DhlDimensions:
    """Represents DHL package dimensions: length, width, height, and units."""

    def __init__(self, dimensions: dict) -> None:
        """Provide a dictionary with keys 'length', 'width', 'height', 'unit'."""
        self.length = dimensions["length"]["value"]
        self.length_unit = dimensions["length"]["unitText"]
        self.width = dimensions["width"]["value"]
        self.width_unit = dimensions["width"]["unitText"]
        self.height = dimensions["height"]["value"]
        self.heigth_unit = dimensions["height"]["unitText"]

    def __str__(self) -> str:
        """Return a string representation of the dimensions."""
        return f"""
            Length: {self.length},
            Width: {self.width},
            Height: {self.height}
        """

    def get_length(self) -> str:
        """Return the length of the package."""
        return self.length

    def get_width(self) -> str:
        """Return the width of the package."""
        return self.width

    def get_height(self) -> str:
        """Return the height of the package."""
        return self.height

    def get_length_unit(self) -> str:
        """Return the unit of the length."""
        return self.length_unit

    def get_width_unit(self) -> str:
        """Return the unit of the width."""
        return self.width_unit

    def get_height_unit(self) -> str:
        """Return the unit of the height."""
        return self.heigth_unit


class DhlDetails:
    """
    Analyze json file "details" part.

    Represents DHL shipment details:
    product name, weight, and dimensions.
    """

    def __init__(self, details: dict) -> None:
        """
        Initialize the DhlDetails object.

        Args:
            details (dict): A dictionary containing shipment details
            from the DHL API's response

        """
        self.product_name = details["product"]["productName"]
        self.weight = (details["weight"]["value"], details["weight"]["unitText"])
        if "dimensions" in details:
            self.dimensions = DhlDimensions(details["dimensions"])
        else:
            self.dimensions = None

    def __str__(self) -> str:
        """Return a string representation of the shipment details."""
        return f"""
            Product Name: {self.product_name},
            Weight: {self.weight},
            Dimensions: {self.dimensions}
        """

    def get_product_name(self) -> str:
        """Return the name of the product."""
        return self.product_name

    def get_weight(self) -> float:
        """Return the weight of the shipment."""
        return float(self.weight[0])

    def get_dimensions(self) -> DhlDimensions | None:
        """Return the three dimensions of the shipment."""
        return self.dimensions
