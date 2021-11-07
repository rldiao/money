import csv

import click
from click.types import File
from sqlalchemy.exc import IntegrityError

from money.controllers import MoneyController
from money.repos import account, entry, transaction

controller = MoneyController(account, transaction, entry)


@click.group()
def cli():
    pass


@cli.command()
@click.argument("name")
def add_account(name: str):
    try:
        controller.create_account(name)
    except IntegrityError as e:
        click.echo(f"Failed to create account because of:\n{e}")


@cli.command()
@click.argument("name")
def get_account(name: str):
    account = controller.get_account(name)
    click.echo(f"Account:\n\tname:\t{account.name}\n\tbudget:\t{account.budget}\n")


@cli.command()
@click.argument("sender")
@click.argument("reciever")
@click.argument("amount", type=click.FLOAT)
def add_transaction(sender: str, reciever: str, amount: float):
    controller.create_transaction(sender, reciever, amount)
    click.echo(f"{sender} -> {reciever} | amount={amount}")


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
