# Usage guide

## 1. Install

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

## 2. Configure credentials

```bash
cp .env.example .env
$EDITOR .env
```

Never commit `.env` files. The project reads credentials from environment variables.

## 3. Run common workflows

Like search results:

```bash
twitter-bot --max-actions 5 engage "open source"
```

Like and repost search results:

```bash
twitter-bot --max-actions 3 engage "python selenium" --retweet
```

Publish a post:

```bash
twitter-bot post "Hello from Selenium"
```

Follow a profile:

```bash
twitter-bot follow openai
```

## Responsible automation

X/Twitter can change its UI without notice, and automated interaction may be limited by platform rules. Use low limits, add review steps where appropriate, and only automate accounts and actions you are authorized to control.
