from sqlalchemy.exc import IntegrityError
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
    ) -> str:
        """Create double entry transaction

        Args:
            sender_name (str): Sender account name
            reciever_name (str): Reciever account name
            amount (float): Amount transacted

        Returns:
            str: Message
        """
        sender = self.account_repo.get_by_name(sender_name)
        reciever = self.account_repo.get_by_name(reciever_name)
        if not sender or not reciever:
            return "Error creating transaction."
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
        return f"Added ${amount:.2f} from {sender.upper()} to {reciever.upper()}"
