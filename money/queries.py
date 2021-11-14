from sqlalchemy import case, func
from sqlalchemy.sql.expression import select

from money.models import Account, Entry, EntryType, Transaction


def getAccountByName(name: str):
    """Get one Account by name"""
    return select(Account).where(Account.name == name).limit(1)


def getUnbalancedTransactions():
    """Get Transactions where entry amounts do not balance to 0"""
    sum_fn = func.sum(
        case(
            [
                (Entry.type == EntryType.CREDIT, Entry.amount),
                (Entry.type == EntryType.DEBIT, -Entry.amount),
            ]
        )
    )
    stmt = (
        select(Transaction, sum_fn)
        .join(Entry)
        .having(sum_fn != 0)
        .group_by(Transaction)
    )
    return stmt
