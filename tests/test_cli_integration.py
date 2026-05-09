from unittest.mock import patch

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
    with patch("ally.cli.uvicorn.run") as mock_run:
        result = runner.invoke(app, ["serve"])

    assert result.exit_code == 0
    assert "http://127.0.0.1:8765" in result.output
    mock_run.assert_called_once_with("ally.server:app", host="127.0.0.1", port=8765)
