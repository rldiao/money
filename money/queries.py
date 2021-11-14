from sqlalchemy.sql.expression import select

from money.models import Account


def getAccountByName(name: str):
    """Get one Account by name"""
    return select(Account).where(Account.name == name).limit(1)
