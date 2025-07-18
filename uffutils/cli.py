import sys
import tempfile

import click

import uffutils
from uffutils.uff.uffdata import UFFData
from uffutils.view import UFFDataViewer


@click.group()
def cli(): ...


@cli.command()
@click.argument("inputfile", type=click.Path(exists=True, allow_dash=True))
@click.option("--nodes", is_flag=True)
def inspect(inputfile: str, nodes: bool):
    data = _get_data(inputfile)
    view = UFFDataViewer(data)
    if nodes:
        print(view.print_nodes())
    else:
        print(view.print_summary())


@cli.command()
@click.argument(
    "inputfile",
    type=click.Path(exists=True, allow_dash=True),
    required=False,
    default="-",
)
@click.argument(
    "outputfile", type=click.Path(allow_dash=True), required=False, default="-"
)
@click.option("--ids", type=str, default="")
@click.option("--step", type=int, default=0)
@click.option("--max", type=int, default=0)
def subset(
    inputfile: str,
    outputfile: str,
    ids: str,
    step: int,
    max: int,
):
    data = _get_data(inputfile)
    if ids or step or max:
        if ids:
            target_nodes = list(map(int, ids.split(",")))
        else:
            target_nodes = None
        data.subset(target_nodes=target_nodes, step=step, n_max=max)
    _handle_output(data, outputfile)


@cli.command()
@click.argument(
    "inputfile",
    type=click.Path(exists=True, allow_dash=True),
    required=False,
    default="-",
)
@click.argument(
    "outputfile", type=click.Path(allow_dash=True), required=False, default="-"
)
@click.option("--length", type=float, default=1)
def scale(inputfile: str, outputfile: str, length: float):
    data = _get_data(inputfile)
    if abs(length - 1) > 1e-9:
        data.scale(length=length)
    _handle_output(data, outputfile)


@cli.command()
@click.argument(
    "inputfile",
    type=click.Path(exists=True, allow_dash=True),
    required=False,
    default="-",
)
@click.argument(
    "outputfile", type=click.Path(allow_dash=True), required=False, default="-"
)
@click.option("--xyz", nargs=3, type=float, default=(0, 0, 0))
def move(inputfile: str, outputfile: str, xyz: tuple[float, float, float]):
    data = _get_data(inputfile)
    data.translate(*xyz)
    _handle_output(data, outputfile)


def _get_data(path) -> UFFData:
    if path == "-":
        path = sys.stdin.readline().strip()
    return uffutils.read(path)


def _handle_output(data, path):
    if path == "-":
        with tempfile.TemporaryFile() as f:
            path = f.name
    uffutils.write(path, data)
    print(path)
