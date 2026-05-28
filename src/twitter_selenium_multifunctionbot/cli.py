"""Command-line interface for the Twitter Selenium bot."""

from __future__ import annotations

import logging
from pathlib import Path

import click

from twitter_selenium_multifunctionbot.config import BotConfig, BrowserName, load_dotenv


def _build_config(
    browser: BrowserName,
    headless: bool,
    max_actions: int,
    profile_directory: Path | None,
) -> BotConfig:
    load_dotenv()
    return BotConfig(
        browser=browser,
        headless=headless,
        max_actions_per_run=max_actions,
        profile_directory=profile_directory,
    )


@click.group(context_settings={"help_option_names": ["-h", "--help"]})
@click.option(
    "--browser",
    type=click.Choice([item.value for item in BrowserName]),
    default="chrome",
)
@click.option(
    "--headless/--no-headless",
    default=False,
    help="Run the browser without a visible UI.",
)
@click.option("--max-actions", default=10, show_default=True, help="Safety limit per command.")
@click.option("--profile-directory", type=click.Path(path_type=Path), default=None)
@click.option("--log-level", default="INFO", show_default=True)
@click.pass_context
def main(
    ctx: click.Context,
    browser: str,
    headless: bool,
    max_actions: int,
    profile_directory: Path | None,
    log_level: str,
) -> None:
    """Automate selected X/Twitter workflows with Selenium."""

    logging.basicConfig(
        level=getattr(logging, log_level.upper(), logging.INFO),
        format="%(levelname)s: %(message)s",
    )
    ctx.obj = _build_config(BrowserName(browser), headless, max_actions, profile_directory)


@main.command()
@click.argument("keyword")
@click.option("--retweet/--no-retweet", default=False)
@click.option("--like/--no-like", "like_posts", default=True)
@click.pass_obj
def engage(config: BotConfig, keyword: str, retweet: bool, like_posts: bool) -> None:
    """Log in, search KEYWORD, and like and/or repost results."""

    from twitter_selenium_multifunctionbot.twitter_bot import TwitterBot

    with TwitterBot(config) as bot:
        bot.login()
        if like_posts:
            result = bot.like_search_results(keyword)
            click.echo(f"Liked {result.succeeded}/{result.attempted}; skipped {result.skipped}.")
        if retweet:
            result = bot.retweet_search_results(keyword)
            click.echo(f"Reposted {result.succeeded}/{result.attempted}; skipped {result.skipped}.")


@main.command("post")
@click.argument("text")
@click.pass_obj
def post(config: BotConfig, text: str) -> None:
    """Log in and publish TEXT as a new post."""

    from twitter_selenium_multifunctionbot.twitter_bot import TwitterBot

    with TwitterBot(config) as bot:
        bot.login()
        bot.post_tweet(text)
        click.echo("Post submitted.")


@main.command("follow")
@click.argument("username")
@click.pass_obj
def follow(config: BotConfig, username: str) -> None:
    """Log in and follow USERNAME."""

    from twitter_selenium_multifunctionbot.twitter_bot import TwitterBot

    with TwitterBot(config) as bot:
        bot.login()
        bot.follow_profile(username)
        click.echo(f"Follow flow completed for {username}.")


if __name__ == "__main__":
    main()
