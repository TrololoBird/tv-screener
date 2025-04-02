from typer.testing import CliRunner
from tv_screener.cli import app

runner = CliRunner()

def test_generate_help():
    result = runner.invoke(app, ["generate", "--help"])
    assert result.exit_code == 0
    assert "--market" in result.output