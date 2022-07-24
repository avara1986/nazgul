import click

from nazgul.service import Nazgul

@click.group()
@click.option('--debug/--no-debug', default=False)
@click.pass_context
def cli(ctx, debug):
    ctx.obj = Nazgul()


@cli.command()
@click.argument('msg')
@click.pass_obj
def task(naz, msg):
    naz.insert_task(msg)

@cli.command()
@click.pass_obj
def init(naz):
    naz.create_db()




if __name__ == '__main__':
    cli()
