# ruff: noqa: PLR2004

from pathlib import Path

import pytest
import typer

from src.validation import (
    COMMENT,
    STRIKE,
    Command,
    parse_command,
    validate_filename,
    validate_interface,
    validate_port,
)


def test_validate_interface() -> None:
    """Accepts IPv4 and IPv6 addresses and rejects non-IP interface strings."""
    assert validate_interface('127.0.0.1') == '127.0.0.1'
    assert validate_interface('::1') == '::1'
    with pytest.raises(typer.BadParameter):
        validate_interface('not_an_ip')


def test_validate_port() -> None:
    """Accepts `1..65535` and rejects out-of-range values."""
    assert validate_port(1) == 1
    assert validate_port(2000) == 2000
    assert validate_port(65535) == 65535
    with pytest.raises(typer.BadParameter):
        validate_port(0)
    with pytest.raises(typer.BadParameter):
        validate_port(65536)


def test_strike_regex() -> None:
    """Matches valid strike moves and rejects invalid squares."""
    assert STRIKE.fullmatch('a2-a4')
    assert STRIKE.fullmatch('h7-h5')
    assert STRIKE.fullmatch('A2-a4')
    assert not STRIKE.fullmatch('a9-a1')


def test_comment_regex() -> None:
    """Matches lines starting with `//` and rejects others."""
    assert COMMENT.fullmatch('//')
    assert COMMENT.fullmatch('// This is a comment')
    assert not COMMENT.fullmatch('This is not a comment')


def test_validate_filename(tmp_path: Path) -> None:
    """Accepts existing files, passes `None` through, and rejects missing."""
    f = tmp_path / 'moves.txt'
    f.write_text('a2-a4\n', encoding='utf-8')
    assert validate_filename(f) == f.expanduser().resolve()
    assert validate_filename(None) is None
    with pytest.raises(typer.BadParameter):
        validate_filename(tmp_path / 'missing.txt')


def test_parse_command() -> None:
    """Parses known commands and rejects unknown ones."""
    assert parse_command('display_board') is Command.DISPLAY_BOARD
    assert parse_command('unknown') is None
