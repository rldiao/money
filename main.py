import click
from sqlalchemy.exc import IntegrityError

from money import crud
from money.models import Transaction
from money.db.session import SessionLocal


@click.group()
def cli():
    pass


@cli.command()
@click.argument("name")
def add_account(name: str):
    try:
        with SessionLocal() as db:
            account = crud.account.create(db, name)
    except IntegrityError as e:
        click.echo(f"Failed to create account because of:\n{e}")
        return
    click.echo(f"Created account: {account.name}")


if __name__ == "__main__":
    cli()
