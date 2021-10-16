from datetime import date

from money.models import Entry
from sqlalchemy.orm.session import Session

from money.models.account import Account
from money.models.entry import EntryType
from money.models.transaction import Transaction


def create(
    db: Session,
    account: Account,
    transaction: Transaction,
    type: EntryType,
) -> Entry:
    entry = Entry(account=account, transaction=transaction, type=type)
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry
