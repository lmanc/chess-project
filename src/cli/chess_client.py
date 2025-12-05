import ipaddress
import socket
import sys
from collections.abc import Callable
from pathlib import Path
from typing import Annotated, TextIO

import typer
from loguru import logger
from rich import print  # noqa: A004
from rich.console import Console

from src.validation import validate_filename, validate_interface, validate_port

err_console = Console(stderr=True)

app = typer.Typer(
    add_completion=False,
    context_settings={'help_option_names': ['-h', '--help']},
)


@app.command()
def main(
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
            help='Enable verbose logging.',
            show_default=False,
        ),
    ] = False,
    log_file: Annotated[
        Path | None,
        typer.Option(
            '--log-file',
            '-l',
            help='Write logs to a file.',
            show_default=False,
        ),
    ] = None,
) -> None:
    """Connect to the chess server and optionally replay a moves file."""
    run_client(
        interface=interface,
        port=port,
        filename=filename,
        verbose=verbose,
        log_file=log_file,
    )


def run_client(
    interface: str = '127.0.0.1',
    port: int = 2000,
    filename: Path | None = None,
    verbose: bool = False,  # noqa: FBT001, FBT002
    log_file: Path | None = None,
    input_func: Callable[[], str] | None = None,
) -> None:
    """Connect and run the client REPL; parameterized for tests."""
    # TODO: add proper error handling for socket errors
    # TODO: support streaming from --filename
    # TODO: print server responses asynchronously
    logger.remove()
    level = 'DEBUG' if verbose else 'INFO'
    if log_file is not None:
        logger.add(str(log_file), level=level)
    else:
        logger.add(sys.stderr, level=level)

    if verbose:
        logger.debug('🔊 Verbose mode enabled')

    if input_func is None:
        input_func = input

    ip = ipaddress.ip_address(interface)
    family = socket.AF_INET6 if ip.version == 6 else socket.AF_INET  # noqa: PLR2004
    server_addr = (interface, port, 0, 0) if ip.version == 6 else (interface, port)  # noqa: PLR2004

    with socket.socket(family, socket.SOCK_STREAM) as sock:
        logger.info('🛰️ Connecting to {}:{} ({})', interface, port, family.name)
        try:
            sock.connect(server_addr)
        except OSError as exc:
            err_msg = exc.strerror or str(exc)
            err_console.print(f'Could not connect to {interface}:{port} {err_msg}')
            raise typer.Exit(code=1) from exc
        logger.info('✅ Connected')

        with sock.makefile('r', encoding='utf-8') as fh:
            while True:
                try:
                    line = input_func()
                except (EOFError, KeyboardInterrupt, StopIteration):
                    logger.info('👋 Disconnecting')
                    break

                msg = line.strip()
                if not msg:
                    continue
                logger.debug('>> {}', msg)
                sock.sendall(f'{msg}\n'.encode())

                response = _read_message(fh)
                if response == '':
                    logger.info('⛔ Server closed the connection')
                    break
                logger.debug('<< {}', response)
                print(response)


def _read_message(fh: TextIO) -> str:
    """Read until a blank line terminator and return the message text."""
    lines: list[str] = []
    for line in fh:
        if line == '\n':
            break
        lines.append(line.rstrip('\n'))
    return '\n'.join(lines)


if __name__ == '__main__':
    app()
