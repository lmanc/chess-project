import chess

from src.protocol import display_board, handle_line


def test_handle_line_legal_move() -> None:
    """Applies a legal move, updates the board, returns a formatted message."""
    board = chess.Board()
    out = handle_line(board, 'e2-e4')
    assert out == '1. White pawn moves from e2 to e4'
    assert len(board.move_stack) == 1


def test_handle_line_illegal_move() -> None:
    """Rejects illegal move and preserves board state."""
    board = chess.Board()
    out = handle_line(board, 'e2-e5')
    assert out == 'Invalid move'
    assert len(board.move_stack) == 0


def test_handle_line_comment() -> None:
    """Acknowledges comments starting with `//`."""
    board = chess.Board()
    out = handle_line(board, '// hello')
    assert out == 'OK'


def test_handle_line_display_board() -> None:
    """Returns ASCII board snapshot for `display_board` command."""
    board = chess.Board()
    snapshot = display_board(board)
    out = handle_line(board, 'display_board')
    assert out == snapshot


def test_handle_line_scan_error() -> None:
    """Returns scan error for unsupported input line."""
    board = chess.Board()
    out = handle_line(board, 'not a thing')
    assert out == 'scan error'
