import re

from parsers.chrome import ChromeParser
from product import Product


class BolParser(ChromeParser):
    def _get_urls_by_keyword_on_page(self, keyword: str, page: int, driver):
        url = f"https://www.bol.com/nl/nl/s/?page={page}&searchtext={keyword}"
        driver.get(url)
        try:
            elements = self._get_elements(driver, '[data-test="product-title"]')
            return [element.get_attribute("href") for element in elements]
        # TODO: selenium exceptions are tricky to intercept
        except Exception:
            return []

    def _get_price(self, driver) -> float:
        price = self._get_element(driver, '[data-test="price"]').text
        price = price.replace('\n', '.')
        price = re.sub(r'[^\d.]', '', price)
        return float(price)

    def get_product_by_url(self, url: str, driver=None) -> Product | None:
        if not driver:
            driver = self._get_driver()
        driver.get(url)

        try:
            title = self._get_element(driver, '[data-test="title"]').text
            price = self._get_price(driver)
            description = self._get_element(driver, '[data-test="product-description"]').text
            image = self._get_element(driver, '[data-test="product-main-image"]').get_attribute("src")

            return Product(
                title,
                description,
                image,
                float(price),
            )
        # TODO: selenium exceptions are tricky to intercept
        except Exception as e:
            return None

    def get_products_by_keyword(self, keyword) -> list[Product]:
        drivers = [self._get_driver() for _ in range(self._settings.CHROME_THREADS)]
        links = self.get_urls_by_keyword(keyword, drivers[0])

        results = self._fetch_concurrently(drivers, links, self.get_product_by_url)
        return results
