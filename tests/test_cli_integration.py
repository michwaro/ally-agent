from pathlib import Path
from unittest.mock import patch

from typer.testing import CliRunner

from afripay.cli import app


def test_scaffold_writes_integration_and_test_files() -> None:
    runner = CliRunner()
    scaffold_code = "# generated integration\nMPESA_MARKER = True\n"
    test_code = "# generated tests\ndef test_mpesa_marker() -> None:\n    assert True\n"
    readme = "# M-Pesa FastAPI\n\nSet MPESA_CONSUMER_KEY before running."

    with runner.isolated_filesystem():
        with (
            patch("afripay.cli.generate_scaffold", return_value=scaffold_code) as mock_scaffold,
            patch("afripay.cli.generate_tests", return_value=test_code) as mock_tests,
            patch("afripay.cli.generate_readme", return_value=readme) as mock_readme,
        ):
            result = runner.invoke(
                app,
                ["scaffold", "--provider", "mpesa", "--framework", "fastapi"],
            )

        integration_path = Path("output/mpesa_fastapi/integration.py")
        test_path = Path("output/mpesa_fastapi/tests/test_integration.py")
        readme_path = Path("output/mpesa_fastapi/README.md")

        assert result.exit_code == 0
        assert integration_path.read_text() == scaffold_code
        assert test_path.read_text() == test_code
        assert readme_path.read_text() == readme
        assert "Scaffold generated successfully" in result.output
        assert str(integration_path) in result.output
        assert str(test_path) in result.output
        assert str(readme_path) in result.output

    mock_scaffold.assert_called_once_with("mpesa", "fastapi")
    mock_tests.assert_called_once_with("mpesa", "fastapi", scaffold_code)
    mock_readme.assert_called_once()
    readme_args = mock_readme.call_args.args
    assert readme_args[:3] == ("mpesa", "fastapi", scaffold_code)
    assert readme_args[3]["verification_method"] == "ip_allowlist+resultcode"
