# Twitter/X Selenium Multifunction Bot

A modern, open-source Python project for carefully automating selected X/Twitter workflows with Selenium **without using the Twitter/X developer API**.

> ⚠️ Use this project responsibly. X/Twitter may restrict automated activity, and its interface can change at any time. Only automate accounts you own or are authorized to manage, keep action limits low, and follow platform rules.

## Features

- Environment-based credential loading; no hard-coded passwords.
- Selenium 4 browser automation with `webdriver-manager` instead of committed driver binaries.
- CLI commands for search engagement, posting, and following.
- Configurable browser, headless mode, profile directory, delays, and per-run action limits.
- Package layout under `src/` with typed configuration and reusable Python API.
- Tests, linting, type checking, GitHub Actions CI, contribution docs, security policy, and MIT license.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
cp .env.example .env
```

Edit `.env` with your account credentials, then run:

```bash
twitter-bot --max-actions 5 engage "python selenium"
```

More examples are available in [docs/USAGE.md](docs/USAGE.md).

## CLI examples

Like search results:

```bash
twitter-bot engage "open source"
```

Like and repost search results:

```bash
twitter-bot --max-actions 3 engage "python" --retweet
```

Publish a post:

```bash
twitter-bot post "Hello from Selenium"
```

Follow a profile:

```bash
twitter-bot follow openai
```

## Python API

```python
from twitter_selenium_multifunctionbot import BotConfig, TwitterBot

config = BotConfig()
with TwitterBot(config) as bot:
    bot.login()
    bot.like_search_results("open source", max_actions=3)
```

## Development

```bash
pip install -e '.[dev]'
ruff check .
mypy src
pytest
```

## Project structure

```text
src/twitter_selenium_multifunctionbot/  # Reusable package code
tests/                                  # Fast tests that do not require live login
docs/                                   # User documentation
.github/workflows/                      # CI configuration
```

## Migration note

The original notebook prototype included hard-coded credentials and a committed ChromeDriver binary. The project is now a reusable package and CLI; credentials are read from `.env`, and drivers are downloaded by `webdriver-manager` at runtime.

## License

MIT. See [LICENSE](LICENSE).
