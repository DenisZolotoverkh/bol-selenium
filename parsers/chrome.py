from abc import ABC, abstractmethod
from concurrent.futures import ThreadPoolExecutor, as_completed

from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import visibility_of_element_located
from selenium.webdriver.support.wait import WebDriverWait

from parsers.base import BaseParser


class ChromeParser(BaseParser, ABC):
    def _get_driver(self) -> Chrome:
        options = Options()
        options.add_argument("--headless=new")
        options.add_argument('--disable-gpu')
        prefs = {
            "profile.managed_default_content_settings.images": 2,
            "profile.default_content_setting_values.media_stream": 2,
            "profile.managed_default_content_settings.javascript": 2
        }

        options.add_experimental_option("prefs", prefs)

        options.binary_location = self._settings.CHROME_EXECUTABLE_LOCATION

        driver = webdriver.Chrome(
            service=Service(self._settings.CHROME_DRIVER_LOCATION),
            options=options
        )
        driver.execute_cdp_cmd("Network.setBlockedURLs", {
            "urls": ["*.png", "*.jpg", "*.jpeg", "*.gif", "*.css", "*.woff", "*.woff2", "*.svg", "*.mp4", "*.js"]
        })
        return driver

    def _get_element(self, driver: Chrome, selector: str):
        return WebDriverWait(driver, self._settings.SELENIUM_COMPONENT_TIMEOUT).until(
            visibility_of_element_located((By.CSS_SELECTOR, selector))
        )

    def _get_elements(self, driver: Chrome, selector: str):
        self._get_element(driver, selector)
        return driver.find_elements(By.CSS_SELECTOR, selector)

    def _fetch_concurrently(self, drivers: list, urls: list[str], fn: callable):
        futures = []
        pool_size = self._settings.CHROME_THREADS

        with ThreadPoolExecutor(max_workers=pool_size) as executor:
            for i, url in enumerate(urls):
                driver_index = i % len(drivers)
                future = executor.submit(fn, url, drivers[driver_index])
                futures.append(future)

        results = []
        for future in as_completed(futures):
            result = future.result()
            if result is not None:
                results.append(result)

        return results

    @abstractmethod
    def _get_urls_by_keyword_on_page(self, keyword: str, page: int, driver):
        pass

    def get_urls_by_keyword(self, keyword: str, driver=None) -> list[str]:
        if not driver:
            driver = self._get_driver()

        page = 1
        result = self._get_urls_by_keyword_on_page(keyword, page, driver)
        urls = []
        while result:
            urls += result
            result = self._get_urls_by_keyword_on_page(keyword, page, driver)
            page += 1
        urls += result

        return urls
