from dataclasses import dataclass
from datetime import date
from typing import List, Protocol


@dataclass
class ParsedTransaction:
    """
    This class exists because we may want to customise the logic that
    determines account logic before creating the SQLAchlemy Transaction model
    """

    transaction_date: date
    amount: float
    memo: str = None
    # Sender account is debited amount
    sender: str = None
    # Reciever account is credited amount
    receiver: str = None


class TransactionParser(Protocol):
    def parse(self) -> List[ParsedTransaction]:
        ...
