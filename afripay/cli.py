"""Command-line interface for AfriPay."""

from pathlib import Path

import typer
from rich.console import Console

from afripay.generator import generate_scaffold, generate_tests

app = typer.Typer(help="Generate secure African payment and communications API scaffolds.")
console = Console()


@app.callback()
def root() -> None:
    """Generate secure African payment and communications API scaffolds."""


@app.command()
def scaffold(
    provider: str = typer.Option(..., "--provider", help="Provider name, for example mpesa."),
    framework: str = typer.Option(..., "--framework", help="Target framework, for example fastapi."),
) -> None:
    """Generate scaffold and test files for a provider and framework."""
    scaffold_code = generate_scaffold(provider, framework)
    output_dir = Path("output") / f"{provider}_{framework}"
    tests_dir = output_dir / "tests"
    integration_path = output_dir / "integration.py"
    test_path = tests_dir / "test_integration.py"

    tests_dir.mkdir(parents=True, exist_ok=True)
    integration_path.write_text(scaffold_code)

    test_code = generate_tests(provider, framework, scaffold_code)
    test_path.write_text(test_code)

    console.print("[green]Scaffold generated successfully[/green]")
    console.print(f"Integration: {integration_path}")
    console.print(f"Tests: {test_path}")


def main() -> None:
    """Run the AfriPay CLI."""
    app()
