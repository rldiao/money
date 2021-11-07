from abc import ABC
from typing import Any, Generic, Optional, Type, TypeVar

from sqlalchemy.orm.session import Session

from money.db.base_class import Base
from money.models import Account, Entry, Transaction

ModelType = TypeVar("ModelType", bound=Base)


class AbstractRepo(ABC, Generic[ModelType]):
    model: Type[ModelType] = None

    def __init__(self) -> None:
        assert self.model is not None, "Please set class attribute 'model'"

    def insert(self, db: Session, obj: ModelType) -> ModelType:
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.id == id).scalar()

    def update(self, db: Session, obj: ModelType) -> ModelType:
        # TODO: Implement update
        raise NotImplementedError()

    def delete(self, db: Session, obj: ModelType) -> ModelType:
        # TODO: Implement delete
        raise NotImplementedError()


class AccountRepo(AbstractRepo[Account]):
    model = Account

    def get_by_name(self, db: Session, name: str) -> Optional[Account]:
        return db.query(self.model).filter(self.model.name == name).scalar()


class EntryRepo(AbstractRepo[Entry]):
    model = Entry


class TransactionRepo(AbstractRepo[Transaction]):
    model = Transaction


account = AccountRepo()
entry = EntryRepo()
transaction = TransactionRepo()
