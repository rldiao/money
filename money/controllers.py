import csv
from datetime import date

from sqlalchemy.exc import IntegrityError
from money import repos
from money.constant import UNCATEGORIZED_ACCOUNT
from money.parser import TransactionParser

from . import repos
from .models import Account, Entry, EntryType, Transaction


class MoneyController:
    def __init__(self) -> None:
        self.account_repo = repos.account
        self.transaction_repo = repos.transaction
        self.entry_repo = repos.entry

    def create_account(self, name: str) -> str:
        """Create account

        Args:
            name (str): Account name

        Returns:
            str: Message
        """
        try:
            account = repos.account.insert(Account(name=name))
            return f"Created account: {account.name}"
        except IntegrityError:
            return f"Failed to create account: {name}"

    def get_account(self, name: str) -> str:
        """Get account

        Args:
            name (str): Account name

        Returns:
            str: Message
        """
        account = self.account_repo.get_by_name(name)
        return f"Account:\n\tname:\t{account.name}\n\tbudget:\t{account.budget}\n"

    def create_transaction(
        self,
        sender_name: str,
        reciever_name: str,
        amount: float,
        memo: str = None,
        transaction_date: date = None,
        create_account=False,
    ) -> str:
        sender = self.account_repo.get_by_name(sender_name)
        reciever = self.account_repo.get_by_name(reciever_name)

        if not sender and create_account:
            sender = self.account_repo.insert(Account(name=sender_name))
        if not reciever and create_account:
            reciever_name = self.account_repo.insert(Account(name=reciever_name))

        err_message = "Error creating transaction due to no account named {}."
        if not sender:
            return err_message.format(sender_name)
        if not reciever:
            return err_message.format(reciever_name)

        transaction = repos.transaction.insert(
            Transaction(transaction_date=transaction_date, memo=memo)
        )
        self.entry_repo.insert(
            Entry(
                account=sender,
                transaction=transaction,
                type=EntryType.DEBIT,
                amount=amount,
            ),
        )
        self.entry_repo.insert(
            Entry(
                account=reciever,
                transaction=transaction,
                type=EntryType.CREDIT,
                amount=amount,
            ),
        )
        return (
            f"Added ${amount:.2f} from {sender_name.upper()} to {reciever_name.upper()}"
        )

    def load_transactions(
        self,
        csvfile,
        parser: TransactionParser,
        create_account: bool,
    ):
        resp = list()
        for transaction in parser.parse(csvfile):
            resp.append(
                self.create_transaction(
                    sender_name=transaction.sender,
                    reciever_name=transaction.receiver,
                    amount=float(transaction.amount),
                    memo=transaction.memo,
                    transaction_date=transaction.transaction_date,
                    create_account=create_account,
                )
            )
        return "\n".join(resp)
