"""High-level X/Twitter Selenium automation workflows."""

from __future__ import annotations

import logging
import time
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import quote_plus

from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver, WebElement
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from twitter_selenium_multifunctionbot.browser import create_driver
from twitter_selenium_multifunctionbot.config import BotConfig

LOGGER = logging.getLogger(__name__)
X_HOME_URL = "https://x.com/home"
X_LOGIN_URL = "https://x.com/i/flow/login"


@dataclass(frozen=True)
class ActionResult:
    """Result of a repeated timeline action."""

    attempted: int
    succeeded: int
    skipped: int


class TwitterBot:
    """A cautious Selenium wrapper for common X/Twitter workflows."""

    def __init__(self, config: BotConfig, driver: WebDriver | None = None) -> None:
        self.config = config
        self.driver = driver or create_driver(config)
        self.wait = WebDriverWait(self.driver, 20)

    def __enter__(self) -> TwitterBot:
        return self

    def __exit__(self, *_exc: object) -> None:
        self.close()

    def close(self) -> None:
        """Close the browser session."""

        self.driver.quit()

    def login(self) -> None:
        """Log in with credentials from configuration."""

        self.driver.get(X_LOGIN_URL)
        self._type_into_visible_input(self.config.username)
        self._click_by_text("Next")

        if self.config.verification:
            try:
                self._type_into_visible_input(self.config.verification, timeout=5)
                self._click_by_text("Next", timeout=5)
            except TimeoutException:
                LOGGER.debug("No extra verification prompt was displayed.")

        password = self.wait.until(
            ec.visibility_of_element_located((By.CSS_SELECTOR, "input[type='password']"))
        )
        password.clear()
        password.send_keys(self.config.password)
        self._click_by_text("Log in")
        self.wait.until(lambda driver: "login" not in driver.current_url.lower())

    def open_search(self, keyword: str, *, latest: bool = False) -> None:
        """Open the X/Twitter search results page for a keyword."""

        tab = "&f=live" if latest else ""
        self.driver.get(f"https://x.com/search?q={quote_plus(keyword)}&src=typed_query{tab}")
        self.wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, "article")))

    def open_profile(self, username: str) -> None:
        """Open an X/Twitter profile by username."""

        self.driver.get(f"https://x.com/{username.lstrip('@')}")
        self.wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, "main")))

    def post_tweet(self, text: str) -> None:
        """Publish a new post from the home composer."""

        self.driver.get(X_HOME_URL)
        composer = self.wait.until(
            ec.visibility_of_element_located(
                (By.CSS_SELECTOR, "div[data-testid='tweetTextarea_0']")
            )
        )
        composer.click()
        composer.send_keys(text)
        self._click_testid("tweetButtonInline")

    def like_search_results(self, keyword: str, *, max_actions: int | None = None) -> ActionResult:
        """Like posts from a search timeline."""

        self.open_search(keyword)
        return self._run_timeline_action("like", self._click_testid_factory("like"), max_actions)

    def retweet_search_results(
        self, keyword: str, *, max_actions: int | None = None
    ) -> ActionResult:
        """Repost posts from a search timeline."""

        self.open_search(keyword)

        def retweet() -> None:
            self._click_testid("retweet")
            self._click_testid("retweetConfirm")

        return self._run_timeline_action("retweet", retweet, max_actions)

    def follow_profile(self, username: str) -> None:
        """Follow a profile if the account is not already followed."""

        self.open_profile(username)
        try:
            self._click_testid(f"{username.lstrip('@')}-follow", timeout=5)
        except TimeoutException:
            LOGGER.info(
                "Profile %s does not expose a follow button; it may already be followed.",
                username,
            )

    def save_screenshot(self, name: str = "debug") -> Path:
        """Save a screenshot for troubleshooting and return its path."""

        self.config.screenshot_directory.mkdir(parents=True, exist_ok=True)
        path = self.config.screenshot_directory / f"{name}.png"
        self.driver.save_screenshot(str(path))
        return path

    def _run_timeline_action(
        self,
        label: str,
        action: Callable[[], None],
        max_actions: int | None,
    ) -> ActionResult:
        limit = max_actions or self.config.max_actions_per_run
        succeeded = 0
        skipped = 0

        for attempted in range(1, limit + 1):
            try:
                action()
                succeeded += 1
                LOGGER.info("%s action %s/%s succeeded", label, attempted, limit)
            except (NoSuchElementException, TimeoutException, WebDriverException) as exc:
                skipped += 1
                LOGGER.warning("%s action %s/%s skipped: %s", label, attempted, limit, exc)
            time.sleep(self.config.action_delay_seconds)
            self.driver.execute_script(
                "window.scrollBy(0, Math.max(600, window.innerHeight * 0.8));"
            )
            time.sleep(self.config.action_delay_seconds)

        return ActionResult(attempted=limit, succeeded=succeeded, skipped=skipped)

    def _click_testid_factory(self, testid: str) -> Callable[[], None]:
        def click() -> None:
            self._click_testid(testid)

        return click

    def _click_testid(self, testid: str, *, timeout: int = 20) -> None:
        selector = f"[data-testid='{testid}']"
        element = WebDriverWait(self.driver, timeout).until(
            ec.element_to_be_clickable((By.CSS_SELECTOR, selector))
        )
        self.driver.execute_script("arguments[0].click();", element)

    def _click_by_text(self, text: str, *, timeout: int = 20) -> None:
        xpath = f"//span[normalize-space()='{text}']/ancestor::div[@role='button']"
        element = WebDriverWait(self.driver, timeout).until(
            ec.element_to_be_clickable((By.XPATH, xpath))
        )
        self.driver.execute_script("arguments[0].click();", element)

    def _type_into_visible_input(self, value: str, *, timeout: int = 20) -> WebElement:
        element = WebDriverWait(self.driver, timeout).until(
            ec.visibility_of_element_located((By.TAG_NAME, "input"))
        )
        element.clear()
        element.send_keys(value)
        return element
