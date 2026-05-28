"""Configuration models for the Twitter Selenium bot."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path


class BrowserName(str, Enum):
    """Supported Selenium browser backends."""

    CHROME = "chrome"
    FIREFOX = "firefox"
    EDGE = "edge"


def _parse_bool(value: str | None, *, default: bool = False) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _parse_positive_int(name: str, *, default: int) -> int:
    raw = os.getenv(name)
    if raw is None:
        return default
    try:
        value = int(raw)
    except ValueError as exc:
        raise ValueError(f"{name} must be an integer") from exc
    if value <= 0:
        raise ValueError(f"{name} must be greater than zero")
    return value


def load_dotenv(path: Path = Path(".env")) -> None:
    """Load simple KEY=VALUE pairs from a .env file without overwriting the environment."""

    if not path.exists():
        return

    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue
        key, value = stripped.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


@dataclass(frozen=True)
class Settings:
    """Environment-driven settings.

    Values are loaded from environment variables and, when present, from a local
    ``.env`` file. Credentials are intentionally never hard-coded in source code.
    """

    username: str = field(default_factory=lambda: _required_env("TWITTER_USERNAME"))
    password: str = field(default_factory=lambda: _required_env("TWITTER_PASSWORD"))
    verification: str | None = field(default_factory=lambda: os.getenv("TWITTER_VERIFICATION"))
    browser: BrowserName = field(
        default_factory=lambda: BrowserName(os.getenv("TWITTER_BROWSER", BrowserName.CHROME.value))
    )
    headless: bool = field(default_factory=lambda: _parse_bool(os.getenv("TWITTER_HEADLESS")))
    implicit_wait_seconds: int = field(
        default_factory=lambda: _parse_positive_int("TWITTER_IMPLICIT_WAIT_SECONDS", default=5)
    )
    action_delay_seconds: int = field(
        default_factory=lambda: _parse_positive_int("TWITTER_ACTION_DELAY_SECONDS", default=2)
    )
    max_actions_per_run: int = field(
        default_factory=lambda: _parse_positive_int("TWITTER_MAX_ACTIONS_PER_RUN", default=10)
    )


def _required_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise ValueError(f"{name} is required. Copy .env.example to .env and fill it in.")
    return value


@dataclass(frozen=True)
class BotConfig(Settings):
    """Runtime bot configuration used by CLI and Python callers."""

    profile_directory: Path | None = None
    screenshot_directory: Path = Path("screenshots")

    def __post_init__(self) -> None:
        if self.profile_directory is not None:
            object.__setattr__(self, "profile_directory", self.profile_directory.expanduser())
        object.__setattr__(self, "screenshot_directory", self.screenshot_directory.expanduser())
