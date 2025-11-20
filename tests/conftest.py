import pytest
from chess import Board


@pytest.fixture
def board() -> Board:
    """Provide a new `Board`."""
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
