import click

import uffutils.file


@click.group()
def cli(): ...


@cli.command()
@click.argument("inputfile", type=click.Path(exists=True))
def inspect(inputfile: str, fields: str):
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
    inputfile: str,
    outputfile: str,
    node_selection: str,
    node_step: int,
    node_count: int,
):
    data = uffutils.read(inputfile)
    if node_selection or node_step or node_count:
        if node_selection:
            target_nodes = list(map(int, node_selection.split(",")))
        else:
            target_nodes = None
        data.subset(target_nodes=target_nodes, step=node_step, n_max=node_count)
    uffutils.write(outputfile, data)
