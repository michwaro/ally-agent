from pathlib import Path
from unittest.mock import patch

from typer.testing import CliRunner

from afripay.cli import app


def test_scaffold_writes_integration_and_test_files() -> None:
    runner = CliRunner()
    scaffold_code = "# generated integration\nMPESA_MARKER = True\n"
    test_code = "# generated tests\ndef test_mpesa_marker() -> None:\n    assert True\n"

    with runner.isolated_filesystem():
        with (
            patch("afripay.cli.generate_scaffold", return_value=scaffold_code) as mock_scaffold,
            patch("afripay.cli.generate_tests", return_value=test_code) as mock_tests,
        ):
            result = runner.invoke(
                app,
                ["scaffold", "--provider", "mpesa", "--framework", "fastapi"],
            )

        integration_path = Path("output/mpesa_fastapi/integration.py")
        test_path = Path("output/mpesa_fastapi/tests/test_integration.py")

        assert result.exit_code == 0
        assert integration_path.read_text() == scaffold_code
        assert test_path.read_text() == test_code
        assert "Scaffold generated successfully" in result.output
        assert str(integration_path) in result.output
        assert str(test_path) in result.output

    mock_scaffold.assert_called_once_with("mpesa", "fastapi")
    mock_tests.assert_called_once_with("mpesa", "fastapi", scaffold_code)
