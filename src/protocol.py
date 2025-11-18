import chess

from src.constants import LETTERS, PIECE_NAME, SEPARATOR
from src.validation import COMMENT, STRIKE, Command, parse_command


def handle_line(board: chess.Board, line: str) -> str:
    """Return the response for an input line and update board if needed."""
    line = line.strip()

    if STRIKE.fullmatch(line):
        move = chess.Move.from_uci(line.replace('-', ''))

        if board.is_legal(move):
            move_no = board.fullmove_number
            piece = board.piece_at(move.from_square)
            color = 'white' if piece.color == chess.WHITE else 'black'
            name = PIECE_NAME[piece.piece_type]
            src = chess.square_name(move.from_square)
            dst = chess.square_name(move.to_square)

            board.push(move)

            return f"{move_no}. {color.title()} {name} moves from {src} to {dst}"

        return 'Invalid move'

    if COMMENT.fullmatch(line):
        return 'OK'

    cmd = parse_command(line)
    if cmd == Command.DISPLAY_BOARD:
        return display_board(board)

    return 'scan error'


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
