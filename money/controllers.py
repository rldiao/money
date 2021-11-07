from typing import Optional
import click
from sqlalchemy.orm.session import Session

from money import repos

from .repos import AccountRepo, EntryRepo, TransactionRepo
from .models import Account, Entry, EntryType, Transaction


class MoneyController:
    def __init__(
        self,
        account_repo: AccountRepo,
        transaction_repo: TransactionRepo,
        entry_repo: EntryRepo,
    ) -> None:
        self.account_repo = account_repo
        self.transaction_repo = transaction_repo
        self.entry_repo = entry_repo

    def create_account(self, name: str) -> Account:
        return repos.account.insert(Account(name=name))

    def get_account(self, name: str) -> Optional[Account]:
        return self.account_repo.get_by_name(name)

    def create_transaction(
        self,
        sender_name: str,
        reciever_name: str,
        amount: float,
    ) -> Transaction:
        sender = self.account_repo.get_by_name(sender_name)
        reciever = self.account_repo.get_by_name(reciever_name)
        transaction = repos.transaction.insert(Transaction())
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
        return transaction
