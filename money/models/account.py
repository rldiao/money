from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import true
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Float, Integer, String

from ..db.base_class import Base


class Account(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=true)
    budget = Column(Float)

    transactions = relationship(
        "Transaction", cascade="all, delete-orphan", back_populates="account"
    )
