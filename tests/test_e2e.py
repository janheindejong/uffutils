from click.testing import CliRunner

from uffutils.cli import cli

from .data import datasets


def test_inspect(): 
	runner = CliRunner() 
	result = runner.invoke(cli, ["inspect", str(datasets["large"]["path"])])
	assert result.exit_code == 0
	assert result.output == """Nodes:
  Number of nodes: 21521
  Nodes: 101, 102, ..., 15835001, 15838001
Sets:
  Set count: 51
  Type count: 15 (1), 55 (50)
  Types: 15, 55, ..., 55, 55
"""
