class DhlDetails:
    def __init__(self, details):
        self.product_name = details["product"]["productName"]
        self.weight = (details["weight"]["value"], details["weight"]["unitText"])
        self.dimensions = DhlDimensions(details["dimensions"])

    def __str__(self):
        return f"""
            Product Name: {self.product_name},
            Weight: {self.weight},
            Dimensions: {self.dimensions}
        """

    def get_product_name(self):
        return self.product_name

    def get_weight(self):
        return self.weight

    def get_dimensions(self):
        return self.dimensions


class DhlDimensions:
    def __init__(self, dimensions):
        """
        :param dimensions: dictionary with keys 'length', 'width', 'height', 'unit'
        """
        self.length = dimensions["length"]["value"]
        self.length_unit = dimensions["length"]["unitText"]
        self.width = dimensions["width"]["value"]
        self.width_unit = dimensions["width"]["unitText"]
        self.height = dimensions["height"]["value"]
        self.heigth_unit = dimensions["height"]["unitText"]

    def __str__(self):
        return f"""
            Length: {self.length},
            Width: {self.width},
            Height: {self.height}
        """

    def get_length(self):
        return self.length

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def get_length_unit(self):
        return self.length_unit

    def get_width_unit(self):
        return self.width_unit

    def get_height_unit(self):
        return self.heigth_unit
