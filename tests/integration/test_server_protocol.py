from src.cli.chess_client import _read_message
from src.protocol.core import _display_board


def test_display_board_roundtrip(server: int, connect, board) -> None:
    """Server returns the board snapshot for the `display_board` command."""
    with connect(server) as sock, sock.makefile('r', encoding='utf-8') as fh:
        sock.sendall(b'display_board\n')
        response = _read_message(fh)

    assert response == _display_board(board)


def test_move_and_invalid_responses(server: int, connect) -> None:
    """Server returns formatted moves and rejects unsupported input."""
    with connect(server) as sock, sock.makefile('r', encoding='utf-8') as fh:
        sock.sendall(b'e2-e4\n')
        assert _read_message(fh) == '1. White pawn moves from e2 to e4'

        sock.sendall(b'not a thing\n')
        assert _read_message(fh) == 'scan error'
