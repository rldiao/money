from money.db.base_class import Base
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Integer, String


class Category(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)

    transactions = relationship("Transaction", back_populates="category")
