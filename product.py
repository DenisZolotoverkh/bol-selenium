from dataclasses import dataclass


@dataclass
class Product:
    title: str
    description: str
    image: str
    price: float
