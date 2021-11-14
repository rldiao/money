from datetime import date
from typing import Optional

from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.session import sessionmaker

from money.models import Account, Entry, EntryType, Transaction
from money.queries import getAccountByName


class AccountNotFound(Exception):
    """Exception raised when Account is not found"""

    def __init__(self, account_name, *args: object) -> None:
        super().__init__(*args)
        self.account_name = account_name


class MoneyApp:
    def __init__(self, sessionmaker: sessionmaker) -> None:
        self.sessionmaker = sessionmaker

    def create_account(self, name: str, budget: float = None):
        """Create new account"""
        account = Account(name=name, budget=budget)
        with self.sessionmaker() as session:
            session.add(account)
            session.commit()

    def get_account(self, name: str) -> Optional[Account]:
        with self.sessionmaker() as session:
            return session.execute(getAccountByName(name)).scalar()

    def add_transaction(
        self,
        sender_name: str,
        reciever_name: str,
        amount: float,
        transaction_date: date = None,
        memo: str = None,
    ):
        """Add transaction and its related entries for each account

        Args:
            sender_name (str): Sender account name
            reciever_name (str): Reciever account name
            amount (float): Amount in transaction
            transaction_date (date, optional): Transaction occurance date. Defaults to None.
            memo (str, optional): Small description of transaction. Defaults to None.

        Raises:
            AccountNotFound: Sender or reciever account does not exist
        """
        with self.sessionmaker() as session:
            try:
                sender = session.execute(getAccountByName(sender_name)).scalar_one()
            except NoResultFound:
                raise AccountNotFound(sender_name)
            try:
                reciever = session.execute(getAccountByName(reciever_name)).scalar_one()
            except NoResultFound:
                raise AccountNotFound(reciever_name)
            entries = [
                Entry(account=sender, type=EntryType.DEBIT, amount=amount),
                Entry(account=reciever, type=EntryType.CREDIT, amount=amount),
            ]
            transaction = Transaction(
                transaction_date=transaction_date,
                memo=memo,
                entries=entries,
            )
            session.add(transaction)
            session.commit()
