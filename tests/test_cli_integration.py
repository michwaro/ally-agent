from typer.testing import CliRunner

from ally.cli import app


def test_submit_prints_placeholder_analysis() -> None:
    runner = CliRunner()
    result = runner.invoke(
        app,
        ["submit", "--report", "test", "--framework", "udhr"],
    )

    assert result.exit_code == 0
    assert "Analysis placeholder" in result.output
    assert "Framework: udhr" in result.output
    assert "Report: test" in result.output


def test_serve_prints_placeholder_message() -> None:
    runner = CliRunner()
    result = runner.invoke(app, ["serve"])

    assert result.exit_code == 0
    assert "Server starting... (coming in Task 3)" in result.output
