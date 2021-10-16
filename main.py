import click
from sqlalchemy.exc import IntegrityError

from money import crud
from money.db.session import SessionLocal
from money.models.entry import EntryType


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
@click.argument("from_acc")
@click.argument("to_acc")
@click.argument("amount", type=click.FLOAT)
def add_transaction(from_acc: str, to_acc: str, amount: float):
    with SessionLocal() as db:
        from_acc_obj = crud.account.get(db, from_acc)
        to_acc_obj = crud.account.get(db, to_acc)
        transaction = crud.transaction.create(db, amount)
        crud.entry.create(db, from_acc_obj, transaction, EntryType.DEBIT)
        crud.entry.create(db, to_acc_obj, transaction, EntryType.CREDIT)
        click.echo(
            f"{from_acc} -> {to_acc} | amount={amount} | {transaction.transaction_date}"
        )


@cli.command()
def load_csv():
    click.echo("Loading transactions from csv...")


if __name__ == "__main__":
    cli()
