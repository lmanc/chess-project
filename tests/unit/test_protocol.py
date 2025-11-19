# ruff: noqa: PLR2004

import chess

from src.protocol import _display_board, process_line


def test_handle_line_legal_move() -> None:
    """Applies a legal move and returns a formatted message."""
    board = chess.Board()
    out = process_line(board, 'e2-e4')
    assert out == '1. White pawn moves from e2 to e4'
    assert len(board.move_stack) == 1


def test_handle_line_capture() -> None:
    """Applies a capture and returns a formatted message."""
    board = chess.Board()
    process_line(board, 'e2-e4')
    process_line(board, 'd7-d5')
    out = process_line(board, 'e4-d5')
    assert out == '2. White pawn on e4 takes black pawn on d5'
    assert len(board.move_stack) == 3


def test_handle_line_en_passant() -> None:
    """Applies an en passant capture and returns a message."""
    board = chess.Board()
    process_line(board, 'e2-e4')
    process_line(board, 'd7-d5')
    process_line(board, 'e4-e5')
    process_line(board, 'f7-f5')
    out = process_line(board, 'e5-f6')
    assert out == '3. White pawn on e5 takes black pawn on f6'
    assert len(board.move_stack) == 5


def test_handle_line_illegal_move() -> None:
    """Rejects illegal move and preserves board state."""
    board = chess.Board()
    out = process_line(board, 'e2-e5')
    assert out == 'Invalid move'
    assert len(board.move_stack) == 0


def test_handle_line_comment() -> None:
    """Acknowledges comments starting with `//`."""
    board = chess.Board()
    out = process_line(board, '// hello')
    assert out == 'OK'


def test_handle_line_display_board() -> None:
    """Returns ASCII board snapshot for `display_board` command."""
    board = chess.Board()
    snapshot = _display_board(board)
    out = process_line(board, 'display_board')
    assert out == snapshot


def test_handle_line_scan_error() -> None:
    """Returns scan error for unsupported input line."""
    board = chess.Board()
    out = process_line(board, 'not a thing')
    assert out == 'scan error'
