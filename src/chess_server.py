import socket
import sys
from typing import Annotated

import chess
import typer
from loguru import logger

from src.validation import COMMENT, STRIKE, validate_interface, validate_port

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
) -> None:
    """Start the chess server and process moves from a single client."""
    logger.remove()
    logger.add(sys.stderr, level="DEBUG" if verbose else "INFO")

    if verbose:
        logger.debug("Verbose mode enabled.")

    board = chess.Board()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        logger.debug("Binding on {}:{}", interface, port)
        s.bind((interface, port))

        logger.info("Listening on {}:{}", interface, port)
        s.listen()

        conn, addr = s.accept()

        with conn, conn.makefile('r', encoding='utf-8') as f:
            logger.info("Connected by {}", addr)

            for raw in f:
                line = raw.strip()
                logger.debug("<< {}", line)

                if STRIKE.fullmatch(line):
                    move = chess.Move.from_uci(line.replace('-', ''))

                    if board.is_legal(move):
                        board.push(move)
                        response = "legal move"
                    else:
                        response = "Invalid move"

                    _reply(conn, response)
                    logger.debug(">> {}", response)
                elif COMMENT.fullmatch(line):
                    _reply(conn, "OK")
                    logger.debug(">> OK")
                else:
                    _reply(conn, "scan error")
                    logger.debug(">> scan error")


def _reply(conn: socket.socket, text: str) -> None:
    conn.sendall((text + "\n").encode("utf-8"))

if __name__ == '__main__':
    app()
