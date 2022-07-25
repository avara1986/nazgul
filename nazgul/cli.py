import pathlib

import click

from nazgul.nazgul import Nazgul

CURRENT_DIR = pathlib.Path(__file__).parent.resolve()
DB_PATH = str(CURRENT_DIR / "db" / "nazgul.db")

@click.group()
@click.option('--debug/--no-debug', default=False)
@click.pass_context
def cli(ctx, debug):
    ctx.obj = Nazgul(DB_PATH)


@cli.command()
@click.argument('msg')
@click.pass_obj
def task(naz, msg: str):
    naz.insert_task(msg, "checkin")

@cli.command()
@click.pass_obj
def init(naz):
    naz.create_db()

@cli.command()
@click.pass_obj
def list(naz):
    results = naz.get_tasks()
    for result in results:
        print(b"ID = " + result["id"])
        print(b"timestamp = " + result["timestamp"])
        print(b"msg = " + result["msg"])
        print(b"check = " + result["check"])

@cli.command()
@click.pass_obj
def week(naz):
    results = naz.get_week_tasks()
    print(results)


if __name__ == '__main__':
    cli()
