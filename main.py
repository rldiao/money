import csv

import click
from click.types import File
from sqlalchemy.exc import IntegrityError

from money import repos
from money.db.session import SessionLocal
from money.models import Account
from money.money import add_double_entry_transaction


@click.group()
def cli():
    pass


@cli.command()
@click.argument("name")
def add_account(name: str):
    try:
        with SessionLocal() as db:
            account = Account(name=name)
            repos.account.insert(db, account)
            click.echo(f"Created account: {account.name}")
    except IntegrityError as e:
        click.echo(f"Failed to create account because of:\n{e}")


@cli.command()
@click.argument("name")
def get_account(name: str):
    with SessionLocal() as db:
        account = repos.account.get_by_name(db, name)
        click.echo(f"Account:\n\tname:\t{account.name}\n\tbudget:\t{account.budget}\n")


@cli.command()
@click.argument("sender")
@click.argument("reciever")
@click.argument("amount", type=click.FLOAT)
def add_transaction(sender: str, reciever: str, amount: float):
    with SessionLocal() as db:
        sender_obj = repos.account.get_by_name(db, sender)
        reciever_obj = repos.account.get_by_name(db, reciever)
        add_double_entry_transaction(db, sender_obj, reciever_obj, amount)
        click.echo(f"{sender} -> {reciever} | amount={amount}")


@cli.command()
@click.argument("mode", type=click.Choice(["westpac"]))
@click.argument("csvfile", type=click.File())
def load_csv(mode: str, csvfile: File):
    click.echo("Loading transactions from csv...")
    reader = csv.DictReader(csvfile)
    if mode == "westpac":
        with SessionLocal() as db:
            try:
                repos.account.insert(db, Account(name="westpac-pay"))
                repos.account.insert(db, Account(name="uncategorized"))
            except IntegrityError:
                pass
            westpac = repos.account.get_by_name(db, "westpac-pay")
            uncategorized = repos.account.get_by_name(db, "uncategorized")
            for row in reader:
                credit = row["Credit Amount"]
                debit = row["Debit Amount"]
                print("Credit:", credit, "Debit:", debit)
                if debit:
                    add_double_entry_transaction(db, westpac, uncategorized, debit)


if __name__ == "__main__":
    cli()
