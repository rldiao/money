from sqlalchemy.orm.session import Session

from money import repos

from .models import Account, Entry, EntryType, Transaction


def add_double_entry_transaction(
    db: Session,
    sender: Account,
    reciever: Account,
    amount: float,
) -> None:
    transaction = Transaction()
    repos.transaction.insert(db, transaction)
    repos.entry.insert(
        db,
        Entry(
            account=sender,
            transaction=transaction,
            type=EntryType.DEBIT,
            amount=amount,
        ),
    )
    repos.entry.insert(
        db,
        Entry(
            account=reciever,
            transaction=transaction,
            type=EntryType.CREDIT,
            amount=amount,
        ),
    )
