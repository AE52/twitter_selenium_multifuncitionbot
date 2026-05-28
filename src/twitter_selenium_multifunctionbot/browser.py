"""Browser factory utilities."""

from __future__ import annotations

from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.remote.webdriver import WebDriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

from twitter_selenium_multifunctionbot.config import BotConfig, BrowserName


def create_driver(config: BotConfig) -> WebDriver:
    """Create a Selenium WebDriver using webdriver-manager.

    The project does not vendor browser-driver binaries. ``webdriver-manager``
    downloads a compatible driver at runtime and keeps the repository small.
    """

    if config.browser is BrowserName.FIREFOX:
        options = webdriver.FirefoxOptions()
        if config.headless:
            options.add_argument("--headless")
        if config.profile_directory:
            options.add_argument("-profile")
            options.add_argument(str(config.profile_directory))
        driver = webdriver.Firefox(
            service=FirefoxService(GeckoDriverManager().install()),
            options=options,
        )
    elif config.browser is BrowserName.EDGE:
        options = webdriver.EdgeOptions()
        if config.headless:
            options.add_argument("--headless=new")
        if config.profile_directory:
            options.add_argument(f"--user-data-dir={config.profile_directory}")
        driver = webdriver.Edge(
            service=EdgeService(EdgeChromiumDriverManager().install()),
            options=options,
        )
    else:
        options = webdriver.ChromeOptions()
        if config.headless:
            options.add_argument("--headless=new")
        if config.profile_directory:
            options.add_argument(f"--user-data-dir={config.profile_directory}")
        options.add_argument("--disable-notifications")
        options.add_argument("--start-maximized")
        driver = webdriver.Chrome(
            service=webdriver.ChromeService(ChromeDriverManager().install()),
            options=options,
        )

    driver.implicitly_wait(config.implicit_wait_seconds)
    return driver
