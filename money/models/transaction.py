from sqlalchemy.orm import relationship
from sqlalchemy.sql.functions import func
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Date, Float, Integer, String

from ..db.base_class import Base


class Transaction(Base):
    id = Column(Integer, primary_key=True)
    transaction_date = Column(Date, nullable=False, default=func.now())
    amount = Column(Float, nullable=False)
    memo = Column(String, nullable=True)

    entries = relationship("Entry", back_populates="transaction")
