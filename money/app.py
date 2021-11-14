from sqlalchemy import select
from sqlalchemy.orm.session import sessionmaker

from money.models import Account


class MoneyApp:
    def __init__(self, sessionmaker: sessionmaker) -> None:
        self.sessionmaker = sessionmaker

    def create_account(self, name: str, budget: float = None):
        """Create new account"""
        account = Account(name=name, budget=budget)
        with self.sessionmaker() as session:
            session.add(account)
            session.commit()

    def get_account(self, name: str) -> Account:
        s = select(Account).where(Account.name == name).limit(1)
        with self.sessionmaker() as session:
            return session.execute(s).scalar()

    def add_transaction(self):
        """Add transaction and its related entries for each account"""
