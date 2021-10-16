from sqlalchemy.orm.session import Session
from money.models.account import Account


def create(db: Session, name: str, budget: float = None):
    account = Account(name=name, budget=budget)
    db.add(account)
    db.commit()
    db.refresh(account)
    return account
