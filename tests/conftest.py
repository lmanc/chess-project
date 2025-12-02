import errno
import socket
import threading
import time
from queue import Empty, Queue

import pytest
from chess import Board

from src.cli import chess_server


@pytest.fixture
def board() -> Board:
    """Provide a new board."""
    return Board()


@pytest.fixture
def white_castling_board() -> Board:
    """Provide a board ready for white castling."""
    return Board('r3k2r/8/8/8/8/8/8/R3K2R w KQkq - 0 1')


@pytest.fixture
def black_castling_board() -> Board:
    """Provide a board ready for black castling."""
    return Board('r3k2r/8/8/8/8/8/8/R3K2R b KQkq - 0 1')


@pytest.fixture
def valid_comment() -> str:
    """Provide a valid comment string."""
    return '// This is a comment'


@pytest.fixture
def invalid_comment() -> str:
    """Provide an invalid comment string."""
    return 'This is not a comment'


@pytest.fixture
def server():
    """Start the server on a random port and ensure it shuts down cleanly."""
    port_queue: Queue[int] = Queue()
    errors: Queue[BaseException] = Queue()

    def target():
        try:
            chess_server.serve(interface='127.0.0.1', port=0, port_queue=port_queue)
        except BaseException as exc:  # noqa: BLE001
            errors.put(exc)

    thread = threading.Thread(target=target, daemon=True)
    thread.start()

    try:
        port = port_queue.get(timeout=2)
    except Empty:
        pytest.fail('Server did not report a listening port in time.')

    yield port

    thread.join(timeout=2)
    if not errors.empty():
        raise errors.get()
    assert not thread.is_alive(), 'Server thread did not exit cleanly.'


@pytest.fixture
def connect():
    """Retrying connector to the test server."""

    def _connect(port: int) -> socket.socket:
        deadline = time.time() + 2.0
        while time.time() < deadline:
            try:
                return socket.create_connection(('127.0.0.1', port), timeout=0.5)
            except OSError as e:
                if e.errno in (errno.ECONNREFUSED, errno.ECONNABORTED, errno.ECONNRESET):
                    time.sleep(0.02)
                    continue
                raise
        pytest.fail('Could not connect to test server.')

    return _connect
