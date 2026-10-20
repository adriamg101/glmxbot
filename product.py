class Product:
    def __init__(self, name: str, price: float, description: str, category: str, brand: str, colors: list, size_availability: list) -> None:
        self.name = name
        self.price = price
        self.description = description
        self.category = category
        self.brand = brand
        self.colors = colors
        self.size_availability = size_availability
