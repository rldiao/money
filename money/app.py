import csv

import click
from click.types import File
from sqlalchemy.exc import IntegrityError

from money.controllers import MoneyController

controller = MoneyController()


@click.group()
def cli():
    pass


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
def load_csv(mode: str, csvfile: File):
    click.echo("Loading transactions from csv...")
    reader = csv.DictReader(csvfile)
    if mode == "westpac":
        try:
            controller.create_account("westpac-pay")
            controller.create_account("uncategorized")
        except IntegrityError:
            pass
        for row in reader:
            credit = row["Credit Amount"]
            debit = row["Debit Amount"]
            print("Credit:", credit, "Debit:", debit)
            if debit:
                controller.create_transaction(
                    sender_name="westpac-pay",
                    reciever_name="uncategorized",
                    amount=debit,
                )
