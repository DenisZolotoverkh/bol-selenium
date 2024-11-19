from parsers.bol import BolParser
from settings import Settings
from store.json import JsonStore

if __name__ == '__main__':
    settings = Settings()

    products = BolParser(settings) \
        .get_products_by_keyword('milk')

    JsonStore() \
        .save(products, 'products.json')
