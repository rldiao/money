from sqlalchemy.orm.session import Session

from money.db.session import SessionLocal
from money.models import category

from . import crud
from .models.entry import EntryType


def add_double_entry_transaction(
    db: Session, from_acc_name: str, to_acc_name: str, category_name: str, amount: float
):
    from_acc = crud.account.get(db, from_acc_name)
    to_acc = crud.account.get(db, to_acc_name)
    category = crud.category.get(db, category_name)
    if not category:
        raise Exception(f"Cannot find category '{category_name}'")
    transaction = crud.transaction.create(db, amount, category)
    crud.entry.create(db, from_acc, transaction, EntryType.DEBIT)
    crud.entry.create(db, to_acc, transaction, EntryType.CREDIT)
