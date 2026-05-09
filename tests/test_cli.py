from typer.testing import CliRunner

from ally.cli import app


def test_help_shows_submit_and_serve_commands() -> None:
    runner = CliRunner()
    result = runner.invoke(app, ["--help"])

    assert result.exit_code == 0
    assert "submit" in result.output
    assert "serve" in result.output
