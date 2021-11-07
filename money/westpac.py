import csv
from datetime import datetime
from typing import List
from money.constant import UNCATEGORIZED_ACCOUNT

from money.parser import ParsedTransaction, TransactionParser


class WestpacParser(TransactionParser):
    @staticmethod
    def parse(csvfile) -> List[ParsedTransaction]:
        """Parse westpac csv export"""
        parsed = list()
        reader = csv.DictReader(csvfile)
        for row in reader:
            account = row["Bank Account"]
            debit = row["Debit Amount"]
            credit = row["Credit Amount"]
            sender = UNCATEGORIZED_ACCOUNT
            reciever = UNCATEGORIZED_ACCOUNT
            if debit:
                amount = debit
                sender = account
            else:
                amount = credit
                reciever = account
            transaction = ParsedTransaction(
                transaction_date=datetime.strptime(row["Date"], "%d/%m/%Y").date(),
                memo=row["Narrative"],
                amount=float(amount),
                sender=sender,
                receiver=reciever,
            )
            parsed.append(transaction)
        return parsed