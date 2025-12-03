import ipaddress
import socket
import sys
from pathlib import Path
from queue import Queue
from threading import Event, Thread
from typing import Annotated

import chess
import typer
from loguru import logger

from src.protocol import GameOver, process_line
from src.validation import validate_interface, validate_port

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
            help='Interface/IP address to bind.',
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
            help='TCP port to listen on.',
            rich_help_panel='Networking',
        ),
    ] = 2000,
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
    """Start the chess server and process moves from multiple clients."""
    serve(interface=interface, port=port, verbose=verbose, log_file=log_file)


def serve(
    interface: str = '127.0.0.1',
    port: int = 2000,
    verbose: bool = False,  # noqa: FBT001, FBT002
    log_file: Path | None = None,
    port_queue: Queue[int] | None = None,
    stop_event: Event | None = None,
) -> None:
    """Run the TCP listener with extra options for testing."""
    logger.remove()
    level = 'DEBUG' if verbose else 'INFO'
    if log_file is not None:
        logger.add(str(log_file), level=level)
    else:
        logger.add(sys.stderr, level=level)

    if verbose:
        logger.debug('🔊 Verbose mode enabled')

    ip = ipaddress.ip_address(interface)
    family = socket.AF_INET6 if ip.version == 6 else socket.AF_INET  # noqa: PLR2004
    bind_addr = (interface, port, 0, 0) if ip.version == 6 else (interface, port)  # noqa: PLR2004

    with socket.socket(family, socket.SOCK_STREAM) as listener:
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.settimeout(0.2)

        logger.debug('🔌 Binding on {}:{} ({})', interface, port, family.name)
        listener.bind(bind_addr)
        actual_port = listener.getsockname()[1]
        logger.debug('✅ Bound on {}:{}', interface, port)

        logger.info('🛰️ Listening on {}:{}', interface, actual_port)
        listener.listen()

        if port_queue is not None:
            port_queue.put(actual_port)

        client_threads: list[Thread] = []
        try:
            while stop_event is None or not stop_event.is_set():
                try:
                    sock, addr = listener.accept()
                except TimeoutError:
                    continue

                handler = Thread(
                    target=_handle_client,
                    args=(sock, addr),
                    daemon=True,
                )
                handler.start()
                client_threads.append(handler)
        finally:
            for thread in client_threads:
                thread.join(timeout=1.0)


def _handle_client(sock: socket.socket, addr: tuple[str, int]) -> None:
    board = chess.Board()
    with sock, sock.makefile('r', encoding='utf-8') as fh:
        logger.info('🌐 Client connected: {}', addr)

        for raw in fh:
            line = raw.strip()
            logger.debug('<< {}', line)
            try:
                response = process_line(board, line)
            except GameOver as e:
                response = str(e)
                _reply(sock, response)
                logger.debug('>> {}', response)
                logger.info('🏁 Game over, closing connection')
                break
            _reply(sock, response)
            # TODO: handle multiline responses properly
            logger.debug('>> {}', response)

        logger.info('👋 Client disconnected')


def _reply(sock: socket.socket, text: str) -> None:
    sock.sendall(f'{text}\n\n'.encode())


if __name__ == '__main__':
    app()
