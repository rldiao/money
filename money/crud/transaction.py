from datetime import date

from money.models import Transaction
from sqlalchemy.orm.session import Session


def create(
    db: Session,
    amount: float,
    memo: str = None,
    transaction_date: date = None,
) -> Transaction:
    transaction = Transaction(
        transaction_date=transaction_date, amount=amount, memo=memo
    )
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    return transaction
