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


def test_each_client_has_its_own_board(server: int, connect) -> None:
    """Each client connection has an independent board state."""
    with connect(server) as first, first.makefile('r', encoding='utf-8') as first_fh:
        first.sendall(b'e2-e4\n')
        assert _read_message(first_fh) == '1. White pawn moves from e2 to e4'

        first.sendall(b'e7-e5\n')
        assert _read_message(first_fh) == '1. Black pawn moves from e7 to e5'

        with connect(server) as second, second.makefile('r', encoding='utf-8') as second_fh:
            second.sendall(b'e2-e4\n')
            assert _read_message(second_fh) == '1. White pawn moves from e2 to e4'
