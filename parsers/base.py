from abc import ABC, abstractmethod

from product import Product
from settings import Settings


class BaseParser(ABC):
    def __init__(self, settings: Settings):
        self._settings = settings

    @abstractmethod
    def get_urls_by_keyword(self, keyword: str) -> list[str]:
        pass

    @abstractmethod
    def get_product_by_url(self, url: str) -> Product | None:
        pass

    @abstractmethod
    def get_products_by_keyword(self, keyword) -> list[Product]:
        pass
