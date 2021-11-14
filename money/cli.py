import click

from money.app import MoneyApp

app = MoneyApp()


@click.group()
def money():
    pass


@money.command()
def add_account():
    click.echo("Add account")


@money.command()
def get_account():
    click.echo("Get account")


@money.command()
def add_transaction():
    click.echo("Add transaction")
