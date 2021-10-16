from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import Date, Float, Integer, String

from ..db.base_class import Base


class Transaction(Base):
    id = Column(Integer, primary_key=True)
    account_id = Column(
        Integer, ForeignKey("account.id", ondelete="CASCADE"), nullable=False
    )
    transaction_date = Column(Date, nullable=False)
    amount = Column(Float, nullable=False)
    memo = Column(String)

    account = relationship("Account", back_populates="transactions")
    entries = relationship("Entry", back_populates="transaction")
