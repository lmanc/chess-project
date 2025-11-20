# ruff: noqa: PLR2004
import chess

from src.protocol import process_line
from src.protocol.core import display_board


def test_handle_line_legal_move(board) -> None:
    """Applies a legal move and returns a formatted message."""
    out = process_line(board, 'e2-e4')
    assert out == '1. White pawn moves from e2 to e4'
    assert len(board.move_stack) == 1


def test_handle_line_capture(board) -> None:
    """Applies a capture and returns a formatted message."""
    process_line(board, 'e2-e4')
    process_line(board, 'd7-d5')
    out = process_line(board, 'e4-d5')
    assert out == '2. White pawn on e4 takes black pawn on d5'
    assert len(board.move_stack) == 3


def test_handle_line_en_passant(board) -> None:
    """Applies an en passant capture and returns a message."""
    process_line(board, 'e2-e4')
    process_line(board, 'd7-d5')
    process_line(board, 'e4-e5')
    process_line(board, 'f7-f5')
    out = process_line(board, 'e5-f6')
    assert out == '3. White pawn on e5 takes black pawn on f6'
    assert len(board.move_stack) == 5


def test_handle_line_white_kingside_castling(white_castling_board) -> None:
    """Applies white kingside castling and returns a formatted message."""
    out = process_line(white_castling_board, 'e1-g1')
    assert out == '1. White king does a little castling from e1 to g1'
    assert len(white_castling_board.move_stack) == 1


def test_handle_line_white_queenside_castling(white_castling_board) -> None:
    """Applies white queenside castling and returns a formatted message."""
    out = process_line(white_castling_board, 'e1-c1')
    assert out == '1. White king does a big castling from e1 to c1'
    assert len(white_castling_board.move_stack) == 1


def test_handle_line_black_kingside_castling(black_castling_board) -> None:
    """Applies black kingside castling and returns a formatted message."""
    out = process_line(black_castling_board, 'e8-g8')
    assert out == '1. Black king does a little castling from e8 to g8'
    assert len(black_castling_board.move_stack) == 1


def test_handle_line_black_queenside_castling(black_castling_board) -> None:
    """Applies black queenside castling and returns a formatted message."""
    out = process_line(black_castling_board, 'e8-c8')
    assert out == '1. Black king does a big castling from e8 to c8'
    assert len(black_castling_board.move_stack) == 1


def test_handle_line_check_suffix() -> None:
    """Adds check suffix when the move gives check."""
    board = chess.Board('4k3/8/8/8/8/8/8/R3K3 w - - 0 1')
    out = process_line(board, 'a1-a8')
    assert out == '1. White rook moves from a1 to a8. Check'
    assert len(board.move_stack) == 1


def test_handle_line_illegal_move(board) -> None:
    """Rejects illegal move and preserves board state."""
    out = process_line(board, 'e2-e5')
    assert out == 'Invalid move'
    assert len(board.move_stack) == 0


def test_handle_line_comment(board, valid_comment) -> None:
    """Acknowledges valid comments."""
    out = process_line(board, valid_comment)
    assert out == 'OK'


def test_handle_line_display_board(board) -> None:
    """Returns ASCII board snapshot for `display_board` command."""
    snapshot = display_board(board)
    out = process_line(board, 'display_board')
    assert out == snapshot


def test_handle_line_scan_error(board) -> None:
    """Returns scan error for unsupported input line."""
    out = process_line(board, 'not a thing')
    assert out == 'scan error'
