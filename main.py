import click
from sqlalchemy.exc import IntegrityError

from money import crud
from money.db.session import SessionLocal
from money.models import category
from money.models.entry import EntryType
from money.money import add_double_entry_transaction


@click.group()
def cli():
    pass


@cli.command()
@click.argument("name")
def add_account(name: str):
    try:
        with SessionLocal() as db:
            account = crud.account.create(db, name)
            click.echo(f"Created account: {account.name}")
    except IntegrityError as e:
        click.echo(f"Failed to create account because of:\n{e}")
        return


@cli.command()
@click.argument("name")
def get_account(name: str):
    with SessionLocal() as db:
        account = crud.account.get(db, name)
        click.echo(f"Account:\n\tname:\t{account.name}\n\tbudget:\t{account.budget}\n")


@cli.command()
@click.argument("name")
def add_category(name: str):
    with SessionLocal() as db:
        category = crud.category.create(db, name)
        click.echo(f"Created category: {category.name}")


@cli.command()
@click.argument("from_acc")
@click.argument("to_acc")
@click.argument("category")
@click.argument("amount", type=click.FLOAT)
def add_transaction(from_acc: str, to_acc: str, category: str, amount: float):
    with SessionLocal() as db:
        add_double_entry_transaction(db, from_acc, to_acc, category, amount)
        click.echo(f"{from_acc} -> {to_acc} | amount={amount}")


@cli.command()
def load_csv():
    click.echo("Loading transactions from csv...")


if __name__ == "__main__":
    cli()
