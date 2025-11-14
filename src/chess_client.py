import socket
from pathlib import Path
from typing import Annotated

import typer

from src.validation import validate_filename, validate_interface, validate_port

app = typer.Typer(
    add_completion=False,
    context_settings={'help_option_names': ['-h', '--help']},
)


@app.command()
def run(
    interface: Annotated[
        str,
        typer.Option(
            '--interface',
            '-i',
            show_default=True,
            callback=validate_interface,
            help='Interface/IP address to connect to.',
            rich_help_panel='Networking',
        ),
    ] = '127.0.0.1',
    port: Annotated[
        int,
        typer.Option(
            '--port',
            '-p',
            show_default=True,
            callback=validate_port,
            help='TCP port to connect to.',
            rich_help_panel='Networking',
        ),
    ] = 2000,
    filename: Annotated[
        Path | None,
        typer.Option(
            '--filename',
            '-f',
            show_default=False,
            callback=validate_filename,
            help='Path to a moves file to replay. (placeholder)',
            rich_help_panel='Gameplay',
        ),
    ] = None,
    verbose: Annotated[  # noqa: FBT002
        bool,
        typer.Option(
            '--verbose',
            '-v',
            help='Enable verbose logging (placeholder).',
            show_default=False,
        ),
    ] = False,
) -> None:
    """Connect to the chess server and optionally replay a moves file."""
    # TODO: add proper error handling for socket errors
    # TODO: support streaming from --filename
    # TODO: print server responses asynchronously

    if filename is not None:
        typer.echo(':warning: --filename is a placeholder and is ignored for now.')
    if verbose:
        typer.echo(':loud_sound: Verbose mode enabled (placeholder).')

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((interface, port))
        typer.echo(f'Connected to {interface}:{port}.')

        while True:
            try:
                line = input('')
            except (EOFError, KeyboardInterrupt):
                typer.echo('\nDisconnecting.')
                break

            msg = line.strip()
            if not msg:
                continue
            sock.sendall(f'{msg}\n'.encode())


if __name__ == '__main__':
    app()
