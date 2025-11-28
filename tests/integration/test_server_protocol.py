import socket
import threading
import time
from queue import Empty, Queue

import pytest

from src.cli import chess_server
from src.protocol.core import display_board


def test_display_board_roundtrip() -> None:
    """Server returns the full board snapshot for the display_board command."""
    port, thread = _start_server()

    with _connect(port) as sock, sock.makefile('r', encoding='utf-8') as fh:
        sock.sendall(b'display_board\n')
        response = _read_message(fh)

    thread.join(timeout=1)

    assert response == display_board(_new_board())


def test_move_and_invalid_responses() -> None:
    """Server returns formatted moves and rejects unsupported input."""
    port, thread = _start_server()

    with _connect(port) as sock, sock.makefile('r', encoding='utf-8') as fh:
        # Legal move
        sock.sendall(b'e2-e4\n')
        assert _read_message(fh) == '1. White pawn moves from e2 to e4'

        # Unsupported input line
        sock.sendall(b'not a thing\n')
        assert _read_message(fh) == 'scan error'

    thread.join(timeout=1)


def _connect(port: int) -> socket.socket:
    """Connect to localhost:port with retries and a short timeout."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2)
    for _ in range(50):
        try:
            sock.connect(('127.0.0.1', port))
            return sock
        except ConnectionRefusedError:
            time.sleep(0.02)
    pytest.fail('Could not connect to test server')


def _read_message(fh) -> str:
    """Read server response until a blank line terminator."""
    lines: list[str] = []
    for line in fh:
        if line == '\n':
            break
        lines.append(line.rstrip('\n'))
    return '\n'.join(lines)


def _start_server() -> tuple[int, threading.Thread]:
    """Start the chess server and return its bound port and thread."""
    port_queue: Queue[int] = Queue()
    ready = threading.Event()

    thread = threading.Thread(
        target=chess_server.serve,
        kwargs={
            'interface': '127.0.0.1',
            'port': 0,
            'ready_event': ready,
            'port_queue': port_queue,
        },
        daemon=True,
    )
    thread.start()

    if not ready.wait(timeout=2):
        pytest.fail('Server did not start listening')
    try:
        port = port_queue.get_nowait()
    except Empty:
        pytest.fail('Server did not report a listening port')

    return port, thread


def _new_board():
    """Construct a new board without importing chess globally."""
    from chess import Board

    return Board()
