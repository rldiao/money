import csv
from datetime import date
from typing import List, Optional

from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.session import Session, sessionmaker

from money.models import Account, Entry, EntryType, Transaction
from money.parser.transaction import ParsedTransaction
from money.parser.westpac import WestpacParser
from money.queries import getAccountByName, getUnbalancedTransactions


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

    def create_transaction(
        self,
        sender_name: str,
        reciever_name: str,
        amount: float,
        transaction_date: date = None,
        memo: str = None,
    ):
        """Create transaction and its related entries for each account

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
            sender = session.execute(getAccountByName(sender_name)).scalar()
            reciever = session.execute(getAccountByName(reciever_name)).scalar()
            if sender is None:
                raise AccountNotFound(sender_name)
            if reciever is None:
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

    def load_csv(self, file):
        with self.sessionmaker() as session:
            self._create_from_parsed(session, WestpacParser.parse(file))
            session.commit()

    def get_unbalanced_transactions(self):
        with self.sessionmaker() as session:
            return session.execute(getUnbalancedTransactions()).all()

    def _create_from_parsed(
        self,
        session: Session,
        transactions: List[ParsedTransaction],
    ):
        """Create transaction from ParsedTransaction"""
        for transaction in transactions:
            entries = []
            sender = None
            if transaction.sender:
                sender = session.execute(getAccountByName(transaction.sender)).scalar()
                if sender is None:
                    sender = Account(name=transaction.sender)
                entries.append(
                    Entry(
                        account=sender,
                        type=EntryType.DEBIT,
                        amount=transaction.amount,
                    )
                )

            reciever = None
            if transaction.receiver:
                reciever = session.execute(
                    getAccountByName(transaction.receiver)
                ).scalar()
                if reciever is None:
                    reciever = Account(name=transaction.receiver)
                entries.append(
                    Entry(
                        account=reciever,
                        type=EntryType.CREDIT,
                        amount=transaction.amount,
                    )
                )

            session.add(
                Transaction(
                    transaction_date=transaction.transaction_date,
                    memo=transaction.memo,
                    entries=entries,
                )
            )
