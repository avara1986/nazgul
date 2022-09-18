import os

import click
from rich import print
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from nazgul.constants import DB_PATH, NAZGUL_CONFIG_PATH
from nazgul.core import Nazgul

CHECK_IN = "checkin"
CHECK_OUT = "checkout"

KIND_WORKDAY = "workday"
KIND_BREAK = "break"
KIND_LUNCH = "lunch"
KIND_TASK = "task"
KIND_MEET = "meet"


@click.group()
@click.option('--debug/--no-debug', default=False)
@click.pass_context
def cli(ctx, debug):
    ctx.obj = Nazgul(DB_PATH)


@cli.command()
@click.argument('msg')
@click.pass_obj
def task(naz, msg: str):
    naz.insert_task(msg, KIND_TASK, CHECK_IN)


@cli.command()
@click.pass_obj
def workday(naz):
    naz.insert_task("workday", KIND_WORKDAY, CHECK_IN)


@cli.command()
@click.pass_obj
def stop(naz):
    naz.insert_task("break", KIND_BREAK, CHECK_IN)


@cli.command()
@click.pass_obj
def init(naz):
    if not os.path.isdir(NAZGUL_CONFIG_PATH):
        print(f"Create config directory {NAZGUL_CONFIG_PATH}")
        os.makedirs(NAZGUL_CONFIG_PATH, exist_ok=True)
    print(f"Create Database in {DB_PATH}")
    naz.create_db()


@cli.command()
@click.pass_obj
def list(naz):
    results = naz.get_tasks()
    table = Table(title="Tasks")
    table.add_column("Date", justify="left", style="cyan", no_wrap=True)
    table.add_column("Title", style="magenta")
    table.add_column("Kind", justify="left", style="blue")
    table.add_column("Type", justify="left", style="white")
    for result in results:
        table.add_row(
            str(result["timestamp"], encoding="utf-8"),
            str(result["msg"], encoding="utf-8"),
            str(result["kind"], encoding="utf-8"),
            str(result["check"], encoding="utf-8"),
        )
    console = Console()
    console.print(table)


@cli.command()
@click.pass_obj
def week_report(naz):
    result = naz.get_week_report()
    print(
        Panel(
            "[cyan]Days {total_days}. MEAN: {mean}".format(
                total_days=result["total_days"],
                mean=result["mean"],
            ),
            title="Resume",
        )
    )

    table = Table(expand=True)
    table.add_column("Week", justify="left", style="cyan", no_wrap=True)
    table.add_column("Hours", style="magenta")

    for week in result["weeks"]:
        table.add_row(
            week["msg"],
            str(week["hours"])
        )
    console = Console()
    console.print(table)


@cli.command()
@click.pass_obj
def week(naz):
    result = naz.get_week_tasks()
    for day in result["days"]:
        print(
            Panel(
                "[cyan]Day {start}. TIME: {total_time}. REST: {rest_time}. TOTAL: {diff}[/cyan]".format(
                    start=str(day["start"][:10], encoding="utf-8"),
                    total_time="{:.2f}".format(day["total_time"]),
                    rest_time="{:.2f}".format(day["rest_time"]),
                    diff="{:.2f}".format(day["total_time"] - day["rest_time"]),
                ),
                title=str(day["start"], encoding="utf-8"),
                subtitle=str(day["end"], encoding="utf-8"),
            )
        )
        if day["tasks"]:
            table = Table(expand=True)
            table.add_column("Date", justify="left", style="cyan", no_wrap=True)
            table.add_column("Title", style="magenta")
            table.add_column("Kind", justify="left", style="blue")
            table.add_column("Total time", justify="left", style="white")
            for task in day["tasks"]:
                table.add_row(
                    str(task["start"], encoding="utf-8"),
                    str(task["_task"]["msg"], encoding="utf-8"),
                    str(task["_task"]["kind"], encoding="utf-8"),
                    "{:.2f} (0:{} mins)".format(task["total_time"], str(int(task["total_time"] * 60)).zfill(2)),
                )
            console = Console()
            console.print(table)


@cli.command()
@click.pass_obj
def list(naz):
    result = naz.get_list_tasks()
    for day in result["days"]:
        print(
            Panel(
                "[cyan]Day {start}. TIME: {total_time}. REST: {rest_time}. TOTAL: {diff}[/cyan]".format(
                    start=str(day["start"][:10], encoding="utf-8"),
                    total_time="{:.2f}".format(day["total_time"]),
                    rest_time="{:.2f}".format(day["rest_time"]),
                    diff="{:.2f}".format(day["total_time"] - day["rest_time"]),
                ),
                title=str(day["start"], encoding="utf-8"),
                subtitle=str(day["end"], encoding="utf-8"),
            )
        )
        if day["tasks"]:
            table = Table(expand=True)
            table.add_column("Date", justify="left", style="cyan", no_wrap=True)
            table.add_column("Title", style="magenta")
            table.add_column("Kind", justify="left", style="blue")
            table.add_column("Total time", justify="left", style="white")
            for task in day["tasks"]:
                table.add_row(
                    str(task["start"], encoding="utf-8"),
                    str(task["_task"]["msg"], encoding="utf-8"),
                    str(task["_task"]["kind"], encoding="utf-8"),
                    "{:.2f} (0:{} mins)".format(task["total_time"], str(int(task["total_time"] * 60)).zfill(2)),
                )
            console = Console()
            console.print(table)


if __name__ == '__main__':
    cli()
