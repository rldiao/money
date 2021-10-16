from datetime import date

from money.models import Transaction
from sqlalchemy.orm.session import Session

from money.models.category import Category


def create(
    db: Session,
    amount: float,
    category: Category,
    memo: str = None,
    transaction_date: date = None,
) -> Transaction:
    transaction = Transaction(
        transaction_date=transaction_date, amount=amount, memo=memo, category=category
    )
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    return transaction
