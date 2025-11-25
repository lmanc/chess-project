from typer.testing import CliRunner

from src.cli.chess_client import app as client_app
from src.cli.chess_server import app as server_app

runner = CliRunner()


class TestServerCLI:
    """Server CLI tests for help and option validation."""

    def test_server_help_shows_options(self) -> None:
        """Shows server help with expected flags and description."""
        result = runner.invoke(server_app, ['--help'])
        out = result.output
        assert result.exit_code == 0
        assert '-i' in out
        assert '--interface' in out
        assert '-p' in out
        assert '--port' in out
        assert '-v' in out
        assert '--verbose' in out
        assert '-l' in out
        assert '--log-file' in out

    def test_server_short_help(self) -> None:
        """Supports `-h` as a help alias for the server."""
        result = runner.invoke(server_app, ['-h'])
        assert result.exit_code == 0

    def test_server_invalid_interface_errors(self) -> None:
        """Rejects invalid server interface before starting sockets."""
        result = runner.invoke(server_app, ['-i', 'bad_ip'])
        assert result.exit_code != 0

    def test_server_invalid_port_errors(self) -> None:
        """Rejects invalid server port before starting sockets."""
        result = runner.invoke(server_app, ['-p', '70000'])
        assert result.exit_code != 0


class TestClientCLI:
    """Client CLI tests for help and option validation."""

    def test_client_help_shows_options(self) -> None:
        """Shows client help with expected flags and description."""
        result = runner.invoke(client_app, ['--help'])
        out = result.output
        assert result.exit_code == 0
        assert '-i' in out
        assert '--interface' in out
        assert '-p' in out
        assert '--port' in out
        assert '-f' in out
        assert '--filename' in out
        assert '-v' in out
        assert '--verbose' in out
        assert '-l' in out
        assert '--log-file' in out

    def test_client_short_help(self) -> None:
        """Supports `-h` as a help alias for the client."""
        result = runner.invoke(client_app, ['-h'])
        assert result.exit_code == 0

    def test_client_invalid_interface_errors(self) -> None:
        """Rejects invalid client interface before connecting."""
        result = runner.invoke(client_app, ['-i', 'bad_ip'])
        assert result.exit_code != 0

    def test_client_invalid_port_errors(self) -> None:
        """Rejects invalid client port before connecting."""
        result = runner.invoke(client_app, ['-p', '70000'])
        assert result.exit_code != 0
