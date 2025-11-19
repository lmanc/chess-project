import pytest
from chess import Board


@pytest.fixture
def board() -> Board:
    """Provide a new `Board`."""
    return Board()


@pytest.fixture
def valid_comment() -> str:
    """Provide a valid comment string."""
    return '// This is a comment'


@pytest.fixture
def invalid_comment() -> str:
    """Provide an invalid comment string."""
    return 'This is not a comment'
