import socket

import pytest
import typer

from src.cli.chess_client import run_client
from src.protocol.core import _display_board


def test_client_display_board(server: int, board, feeder, capsys) -> None:
    """Client requests a board snapshot and prints it."""
    run_client(interface='127.0.0.1', port=server, input_func=feeder(['display_board']))

    captured = capsys.readouterr()
    assert captured.out.rstrip('\n') == _display_board(board)


def test_client_move_and_invalid(server: int, feeder, capsys, invalid_comment) -> None:
    """Client prints move response and rejects unsupported input."""
    run_client(interface='127.0.0.1', port=server, input_func=feeder(['e2-e4', invalid_comment]))

    captured = capsys.readouterr()
    assert captured.out.splitlines() == [
        '1. White pawn moves from e2 to e4',
        'scan error',
    ]


def test_client_handles_connection_failure_gracefully(feeder, capsys) -> None:
    """Client exits cleanly when server is unavailable."""
    with pytest.raises(typer.Exit):
        run_client(
            interface='127.0.0.1',
            port=2000,
            input_func=feeder(['display_board']),
        )

    captured = capsys.readouterr()
    assert 'Could not connect to 127.0.0.1' in captured.err
