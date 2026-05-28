from pathlib import Path

from twitter_selenium_multifunctionbot.config import BotConfig, BrowserName


def test_config_loads_from_environment(monkeypatch):
    monkeypatch.setenv("TWITTER_USERNAME", "alice")
    monkeypatch.setenv("TWITTER_PASSWORD", "secret")
    monkeypatch.setenv("TWITTER_BROWSER", "firefox")
    monkeypatch.setenv("TWITTER_HEADLESS", "true")

    config = BotConfig()

    assert config.username == "alice"
    assert config.password == "secret"
    assert config.browser is BrowserName.FIREFOX
    assert config.headless is True


def test_config_expands_paths(monkeypatch):
    monkeypatch.setenv("TWITTER_USERNAME", "alice")
    monkeypatch.setenv("TWITTER_PASSWORD", "secret")

    config = BotConfig(profile_directory=Path("~/twitter-profile"))

    assert str(config.profile_directory).startswith(str(Path.home()))
