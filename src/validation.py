import ipaddress
import re

import typer

STRIKE = re.compile(r'[a-h][1-8]-[a-h][1-8]')
COMMENT = re.compile(r'//.*')
COMMAND = ''


def validate_interface(value: str) -> str:
    """Ensure the provided interface value is a valid IP address."""
    try:
        ipaddress.ip_address(value)
    except ValueError as exc:  # pragma: no cover - CLI validation
        msg = 'Interface must be a valid IPv4 or IPv6 address.'
        raise typer.BadParameter(msg) from exc
    return value


def validate_port(value: int) -> int:
    """Ensure the port is within the TCP user range."""
    if not (1 <= value <= 65535):  # noqa: PLR2004
        msg = 'Port must be between 1 and 65535.'
        raise typer.BadParameter(msg)
    return value
