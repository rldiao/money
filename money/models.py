import enum

from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import true
from sqlalchemy.sql.functions import func
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import Date, Enum, Float, Integer, String

from .db.base_class import Base


class Account(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=true)
    budget = Column(Float, nullable=True)

    entries = relationship(
        "Entry", cascade="all, delete-orphan", back_populates="account"
    )

    def __str__(self) -> str:
        return f"Account(name={self.name}, budget={self.budget})"


class EntryType(enum.Enum):
    CREDIT = enum.auto()
    DEBIT = enum.auto()


class Entry(Base):
    id = Column(Integer, primary_key=True)
    account_id = Column(Integer, ForeignKey("account.id"), nullable=False)
    transaction_id = Column(Integer, ForeignKey("transaction.id"), nullable=False)
    type = Column(Enum(EntryType))
    amount = Column(Float, nullable=False)

    transaction = relationship("Transaction", back_populates="entries")
    account = relationship("Account", back_populates="entries")


class Transaction(Base):
    id = Column(Integer, primary_key=True)
    transaction_date = Column(Date, nullable=False, default=func.now())
    memo = Column(String, nullable=True)

    entries = relationship("Entry", back_populates="transaction")
