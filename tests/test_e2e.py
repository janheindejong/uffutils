from click.testing import CliRunner

from uffutils.cli import cli

from .data import datasets


def test_inspect():
    runner = CliRunner()
    result = runner.invoke(cli, ["inspect", str(datasets["large"].path)])
    assert result.exit_code == 0
    assert (
        result.output
        == """Nodes:
  Number of nodes: 21521
  Nodes: 101, 102, ..., 15835001, 15838001
Sets:
  Set count: 51
  Type count: 15 (1), 55 (50)
  Types: 15, 55, ..., 55, 55
"""
    )


def test_rotate():
    runner = CliRunner()
    result = runner.invoke(
        cli, ["rotate", str(datasets["subset"].path), "--angles", "90", "90", "90"]
    )
    assert result.exit_code == 0
    with open(result.output, "r") as f:
        actual = f.read()
    with open(datasets["subset_rotated"].path) as f:
        expected = f.read()
    assert actual == expected
