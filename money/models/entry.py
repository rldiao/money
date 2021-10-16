import enum

from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import Enum, Integer

from ..db.base_class import Base


class EntryType(enum.Enum):
    credit = "C"
    debit = "D"


class Entry(Base):
    id = Column(Integer, primary_key=True)
    account_id = Column(Integer, ForeignKey("account.id"), nullable=False)
    transaction_id = Column(Integer, ForeignKey("transaction.id"), nullable=False)
    type = Column(Enum(EntryType))

    transaction = relationship("Transaction", back_populates="entries")
    account = relationship("Account", back_populates="entries")
