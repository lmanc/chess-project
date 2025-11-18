import chess

from src.validation import COMMENT, STRIKE, Command, parse_command


def handle_line(board: chess.Board, line: str) -> str:
    """Return the response for an input line and update board if needed."""
    line = line.strip()

    if STRIKE.fullmatch(line):
        move = chess.Move.from_uci(line.replace('-', ''))
        if board.is_legal(move):
            board.push(move)
            return 'legal move'
        return 'Invalid move'

    if COMMENT.fullmatch(line):
        return 'OK'

    cmd = parse_command(line)
    if cmd == Command.DISPLAY_BOARD:
        return str(board)

    return 'scan error'
