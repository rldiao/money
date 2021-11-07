from dataclasses import dataclass
from datetime import date
from typing import List, Optional, Protocol

from money.constant import UNCATEGORIZED_ACCOUNT


@dataclass
class ParsedTransaction:
    """
    This class exists because we may want to customise the logic that
    determines account logic before creating a Transaction model
    """

    transaction_date: date
    memo: str
    amount: float
    # Sender account is debited amount
    sender: str
    # Reciever account is credited amount
    receiver: str = UNCATEGORIZED_ACCOUNT


class TransactionParser(Protocol):
    @staticmethod
    def parse(csvfile) -> List[ParsedTransaction]:
        ...
