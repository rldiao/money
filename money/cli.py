import click
from click.types import FLOAT
from sqlalchemy.exc import IntegrityError

from money.app import AccountNotFound, MoneyApp
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
        click.echo(f'Account "{name}" already exists!', err=True)
        return
    click.echo(f"Created account: {name}")


@money.command()
@click.argument("name")
def get_account(name: str):
    account = _app.get_account(name)
    if account is None:
        click.echo(f'There is not account named "{name}"')
        return
    click.echo(account)


@money.command()
@click.argument("sender")
@click.argument("reciever")
@click.argument("amount", type=FLOAT)
def add_transaction(sender: str, reciever: str, amount: float):
    try:
        _app.create_transaction(
            sender_name=sender,
            reciever_name=reciever,
            amount=amount,
        )
    except AccountNotFound as e:
        click.echo(f'Account "{e.account_name}" does not exist!')


@money.command()
@click.argument("csvfile", type=click.File())
def load_csv(csvfile):
    _app.load_csv(csvfile)


@money.command()
def list_unbalanced_transactions():
    output = "Transactions:\n"
    for transaction in _app.get_unbalanced_transactions():
        output += f"\t{transaction[0]}: Missing ${transaction[1]}\n"
    click.echo(output)
