import click
from sqlalchemy.exc import IntegrityError

from money.app import MoneyApp
from money.db.session import SessionLocal

_app = MoneyApp(SessionLocal)


@click.group()
def money():
    pass


@money.command()
@click.argument("name")
def add_account(name: str):
    try:
        _app.create_account(name)
    except IntegrityError:
        click.echo(f'Error: Account "{name}" already exists!', err=True)
        return
    click.echo(f"Created account: {name}")


@money.command()
@click.argument("name")
def get_account(name: str):
    account = _app.get_account(name)
    if account is None:
        click.echo(f'There is not account named "{name}"')
    click.echo(account)


@money.command()
def add_transaction():
    click.echo("Add transaction")
