import click

import uffutils.file


@click.group()
@click.argument("input", click.File("r"))
@click.pass_context
def cli(ctx, input):
    ctx.ensure_object(dict)

    ctx.obj["input"] = input.read()


@cli.command()
@click.argument("path", type=str)
def read(path: str):
    ds = uffutils.file.read(path)
    click.echo(uffutils.file.serialize(ds))


@cli.command()
@click.argument("input", type=str)
@click.argument("path", type=str)
def write(input: str, path: str):
    ds = uffutils.file.deserialize(input)
    path = uffutils.file.write(path, ds, True)
    click.echo(path)


@cli.command()
@click.argument("input", type=str)
@click.option("--step", type=int, default=1)
def nodes(input: str, step: int = 1):
    ...
    # ds = uffutils.file.deserialize(input)
    # nodes = uffutils.nodes.get_nodes(ds, step)
    # click.echo(",".join(map(str, nodes)))


@cli.command()
@click.argument("input", type=str)
@click.option("--nodes", type=str, required=True)
def subset(input: str, nodes: str):
    nodes = set(map(int, nodes.split(",")))
    # data = uffutils.subset.get_subset(input, nodes)
    # click.echo(uffutils.file.serialize(data))
