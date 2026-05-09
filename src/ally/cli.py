"""Command-line interface for Ally."""

import typer
import uvicorn
from rich.console import Console

app = typer.Typer(help="Analyze anonymous community accountability reports.")
console = Console()


@app.callback()
def root() -> None:
    """Analyze anonymous community accountability reports."""


@app.command()
def submit(
    report: str = typer.Option(..., "--report", help="Anonymous community report text."),
    framework: str = typer.Option(..., "--framework", help="Rights framework, for example udhr."),
) -> None:
    """Submit a report for placeholder Ally analysis."""
    console.print("[green]Analysis placeholder[/green]")
    console.print(f"Framework: {framework}")
    console.print(f"Report: {report}")


@app.command()
def serve() -> None:
    """Start the Ally server."""
    console.print("Serving Ally at http://127.0.0.1:8765")
    uvicorn.run("ally.server:app", host="127.0.0.1", port=8765)


def main() -> None:
    """Run the Ally CLI."""
    app()
