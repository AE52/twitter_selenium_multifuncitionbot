from click.testing import CliRunner

from twitter_selenium_multifunctionbot.cli import main


def test_cli_help_renders():
    result = CliRunner().invoke(main, ["--help"])

    assert result.exit_code == 0
    assert "Automate selected X/Twitter workflows" in result.output
    assert "engage" in result.output
