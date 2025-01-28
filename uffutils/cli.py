import click

import uffutils.file


@click.group()
def cli(): ...


@cli.command()
@click.argument("inputfile", type=click.Path(exists=True))
def describe(inputfile: str):
    data = uffutils.file.read(inputfile)
    nodes = data.get_nodes()
    click.echo(",".join(map(str, nodes)))
    # TODO: make a lot better


@cli.command()
@click.argument("inputfile", type=click.Path(exists=True))
@click.argument("outputfile", type=click.Path())
@click.option("--node-selection", type=str, default="")
@click.option("--node-step", type=int, default=0)
@click.option("--node-count", type=int, default=0)
def modify(
    inputfile: str, outputfile: str, nodes: str, nodes_step: int, nodes_count: int
):
    data = uffutils.read(inputfile)
    if nodes or nodes_step or nodes_count:
        if nodes:
            target_nodes = list(map(int, nodes.split(",")))
        else:
            target_nodes = None
        data.subset(target_nodes=target_nodes, step=nodes_step, n_max=nodes_count)
    uffutils.write(outputfile, data)
