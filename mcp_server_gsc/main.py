"""Main entry point for the MCP server."""

import asyncio
import os
import sys
from pathlib import Path
from typing import Optional

import typer

from .config import Config
from .server import GSCMCPServer


app = typer.Typer(
    name="mcp-server-gsc",
    help="MCP server for Google Search Console",
)


@app.command()
def main(
    credentials_path: Optional[Path] = typer.Option(
        None,
        "--credentials",
        "-c",
        help="Path to the Google Cloud credentials file. If not provided, "
        "the GOOGLE_APPLICATION_CREDENTIALS environment variable will be used.",
    ),
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-v",
        help="Enable verbose logging",
    ),
) -> None:
    """Run the MCP server."""
    # Create server configuration
    config = Config(google_credentials_path=str(credentials_path) if credentials_path else None)
    
    # Check for credentials
    if not config.google_credentials:
        typer.echo(
            "Error: Google Search Console credentials not found. "
            "Set the GOOGLE_APPLICATION_CREDENTIALS environment variable "
            "or provide the --credentials option.",
            err=True,
        )
        raise typer.Exit(code=1)
    
    if not config.google_credentials.exists():
        typer.echo(
            f"Error: Credentials file not found: {config.google_credentials}",
            err=True,
        )
        raise typer.Exit(code=1)
    
    if verbose:
        typer.echo(f"Starting MCP server with credentials: {config.google_credentials}")
    
    # Create server instance
    server = GSCMCPServer(config)
    
    # Run the server
    asyncio.run(server.run())


if __name__ == "__main__":
    app()