import chess

from src.constants import LETTERS, PIECE_NAME, SEPARATOR
from src.validation import COMMENT, STRIKE, Command, parse_command


def process_line(board: chess.Board, line: str) -> str:
    """Return the response for an input line and update board if needed."""
    line = line.strip()

    if STRIKE.fullmatch(line):
        return handle_move(board, line)

    if COMMENT.fullmatch(line):
        return 'OK'

    cmd = parse_command(line)
    if cmd == Command.DISPLAY_BOARD:
        return display_board(board)

    return 'scan error'


def handle_move(board: chess.Board, text: str) -> str:
    """Apply a UCI move string if legal and return formatted message."""
    move = chess.Move.from_uci(text.replace('-', ''))
    if not board.is_legal(move):
        return 'Invalid move'

    message = format_move(board, move)

    future = board.copy()
    future.push(move)
    if future.is_check():
        message += '. Check'

    board.push(move)
    return message


def format_move(board: chess.Board, move: chess.Move) -> str:
    """Format a legal move (capture or normal) without mutating the board."""
    move_no = board.fullmove_number
    piece = board.piece_at(move.from_square)
    color = piece_color(piece)
    name = PIECE_NAME[piece.piece_type]
    src = chess.square_name(move.from_square)
    dst = chess.square_name(move.to_square)

    if board.is_castling(move):
        side = 'little' if dst[0] == 'g' else 'big'
        return (
            f'{move_no}. {color.title()} king does a '
            f'{side} castling from {src} to {dst}'
        )

    if board.is_capture(move):
        captured, _ = captured_piece(board, move)
        captured_color = piece_color(captured)
        captured_name = PIECE_NAME[captured.piece_type]

        return (
            f'{move_no}. {color.title()} {name} on {src} '
            f'takes {captured_color} {captured_name} on {dst}'
        )

    return f'{move_no}. {color.title()} {name} moves from {src} to {dst}'


def piece_color(piece: chess.Piece) -> str:
    """Return piece color as a string."""
    return 'white' if piece.color == chess.WHITE else 'black'


def captured_piece(board: chess.Board, move: chess.Move) -> tuple[chess.Piece, chess.Square]:
    """Return the captured piece (handles en passant) and its square."""
    captured = board.piece_at(move.to_square)
    capture_square = move.to_square
    if captured is None and board.is_en_passant(move):
        capture_square = chess.square(
            chess.square_file(move.to_square),
            chess.square_rank(move.from_square),
        )
        captured = board.piece_at(capture_square)
    return captured, capture_square


def display_board(board: chess.Board) -> str:
    """Return an ASCII board snapshot."""
    s = str(board).splitlines()
    s = [f'{i} {line}' for i, line in zip(range(8, 0, -1), s, strict=True)]
    s = [' | '.join(line.replace(' ', '')) + ' |' for line in s]

    temp = []
    for line in s:
        temp.extend([SEPARATOR, line])
    temp.append(SEPARATOR)

    s = [LETTERS, *temp, LETTERS]

    return '\n'.join(s).replace('.', ' ')
