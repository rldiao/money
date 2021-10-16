from sqlalchemy.orm.session import Session
from money.models.account import Account


def create(db: Session, name: str, budget: float = None) -> Account:
    account = Account(name=name, budget=budget)
    db.add(account)
    db.commit()
    db.refresh(account)
    return account


def get(db: Session, name: str) -> Account:
    return db.query(Account).filter(Account.name == name).scalar()
