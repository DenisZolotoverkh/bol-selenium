from settings.selenium import SeleniumSettings


class ChromeSettings(SeleniumSettings):
    CHROME_DRIVER_LOCATION: str
    CHROME_EXECUTABLE_LOCATION: str
    CHROME_THREADS: int
