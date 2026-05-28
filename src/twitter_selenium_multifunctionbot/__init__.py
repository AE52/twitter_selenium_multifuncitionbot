"""Selenium automation helpers for X/Twitter."""

from __future__ import annotations

from typing import Any

from twitter_selenium_multifunctionbot.config import BotConfig, Settings

__all__ = ["BotConfig", "Settings", "TwitterBot"]
__version__ = "0.1.0"


def __getattr__(name: str) -> Any:
    """Lazily import Selenium-dependent classes only when needed."""

    if name == "TwitterBot":
        from twitter_selenium_multifunctionbot.twitter_bot import TwitterBot

        return TwitterBot
    raise AttributeError(name)
