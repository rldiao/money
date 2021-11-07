import click
from click.types import File
from money.constant import UNCATEGORIZED_ACCOUNT

from money.controllers import MoneyController
from money.westpac import WestpacParser

controller = MoneyController()


@click.group()
def cli():
    pass


@cli.command()
def init():
    """Initialize default application data"""
    controller.create_account(UNCATEGORIZED_ACCOUNT)


@cli.command()
@click.argument("name")
def add_account(name: str):
    click.echo(controller.create_account(name))


@cli.command()
@click.argument("name")
def get_account(name: str):
    click.echo(controller.get_account(name))


@cli.command()
@click.argument("sender")
@click.argument("reciever")
@click.argument("amount", type=click.FLOAT)
def add_transaction(sender: str, reciever: str, amount: float):
    click.echo(controller.create_transaction(sender, reciever, amount))


@cli.command()
@click.argument("mode", type=click.Choice(["westpac"]))
@click.argument("csvfile", type=click.File())
@click.option("--create-account", is_flag=True)
def load_csv(mode: str, csvfile: File, create_account):
    click.echo("Loading transactions from csv...")
    if mode == "westpac":
        click.echo(
            controller.load_transactions(
                csvfile,
                WestpacParser(),
                create_account=create_account,
            )
        )
