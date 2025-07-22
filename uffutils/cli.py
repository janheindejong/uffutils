import sys
import tempfile

import click
import numpy as np

import uffutils
from uffutils.uff.uffdata import UFFData
from uffutils.view import UFFDataViewer


@click.group()
def cli(): ...


@cli.command()
@click.argument("inputfile", type=click.Path(exists=True, allow_dash=True))
@click.option("--nodes", is_flag=True, help="Show only list of node ids")
def inspect(inputfile: str, nodes: bool):
    """Inspect data"""
    data = _read_input(inputfile)
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
@click.option("--ids", type=str, default="", help="List of node-ids to select")
@click.option("--step", type=int, default=0, help="Step between nodes")
@click.option("--max", type=int, default=0, help="Maximum number of nodes")
def subset(
    inputfile: str,
    outputfile: str,
    ids: str,
    step: int,
    max: int,
):
    """Create dataset containing a subset of nodes"""
    data = _read_input(inputfile)
    target_nodes = list(map(int, ids.split(","))) if ids else None
    data.subset(target_nodes=target_nodes, step=step, n_max=max)
    _write_output(data, outputfile)


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
@click.option("--length", type=float, default=1, help="Length scaling factor")
def scale(inputfile: str, outputfile: str, length: float):
    """Scale values"""
    data = _read_input(inputfile)
    if abs(length - 1) > 1e-9:
        data.scale(length=length)
    _write_output(data, outputfile)


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
@click.option(
    "--xyz", nargs=3, type=float, default=(0, 0, 0), help="X,Y,Z-translations"
)
def translate(inputfile: str, outputfile: str, xyz: tuple[float, float, float]):
    """Translate data"""
    data = _read_input(inputfile)
    data.translate(*xyz)
    _write_output(data, outputfile)


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
@click.option(
    "--angles",
    nargs=3,
    type=float,
    default=(0, 0, 0),
    help="Roll, pitch & yaw rotations, or extrensic X, Y and Z Tait-Bryan rotations [deg]",
)
def rotate(inputfile: str, outputfile: str, angles: tuple[float, float, float]):
    """Rotate data"""
    data = _read_input(inputfile)
    angles = angles[0] * np.pi / 180, angles[1] * np.pi / 180, angles[2] * np.pi / 180
    data.rotate(angles)
    _write_output(data, outputfile)


def _read_input(path) -> UFFData:
    if path == "-":
        path = sys.stdin.readline().strip()
    return uffutils.read(path)


def _write_output(data, path):
    if path == "-":
        with tempfile.TemporaryFile() as f:
            path = f.name
    uffutils.write(path, data)
    sys.stdout.write(path)
