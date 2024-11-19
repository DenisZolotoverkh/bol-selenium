import json
from dataclasses import asdict

from product import Product
from store.base import BaseStore


class JsonStore(BaseStore):
    def save(self, products: list[Product], filepath: str, *args, **kwargs):
        data = [asdict(product) for product in products]
        with open("products.json", "w") as f:
            json.dump(data, f, indent=4)
