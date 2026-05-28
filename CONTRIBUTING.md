# Contributing

Thanks for improving this project!

## Development setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
```

## Quality checks

Run these before opening a pull request:

```bash
ruff check .
mypy src
pytest
```

## Pull requests

- Keep credentials, cookies, browser profiles, and screenshots out of commits.
- Prefer small, focused pull requests.
- Add tests for behavior that can be tested without a live X/Twitter account.
- Document user-facing changes in `README.md` or `docs/USAGE.md`.
