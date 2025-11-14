import socket
from typing import Annotated

import chess
import typer
from rich import print  # noqa: A004

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
            help='Enable verbose logging (placeholder).',
            show_default=False,
        ),
    ] = False,
) -> None:
    """Start the chess server and process moves from a single client."""
    board = chess.Board()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        if verbose:
            print(':loud_sound: Verbose mode enabled (placeholder).')
        print(f'Binding on {interface}:{port}')
        s.bind((interface, port))
        print(f'Listening on {interface}:{port}')
        s.listen()
        conn, addr = s.accept()
        with conn, conn.makefile('r', encoding='utf-8') as f:
            print(f':globe_with_meridians: Connected by {addr}')
            for line in f:
                line = line.strip()
                if STRIKE.fullmatch(line):
                    move = line.replace('-', '')
                    move = chess.Move.from_uci(move)
                    if board.is_legal(move):
                        print('legal move')
                        board.push(move)
                    else:
                        print('illegal move')
                elif COMMENT.fullmatch(line):
                    conn.sendall(b'comment')
                else:
                    conn.sendall(b'scan error')


if __name__ == '__main__':
    app()
