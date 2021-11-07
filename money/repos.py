from abc import ABC
from typing import Any, Generic, Optional, Type, TypeVar

from sqlalchemy.orm.session import sessionmaker

from money.db.base_class import Base
from money.db.session import SessionLocal
from money.models import Account, Entry, Transaction

ModelType = TypeVar("ModelType", bound=Base)


class AbstractRepo(ABC, Generic[ModelType]):
    model: Type[ModelType] = None

    def __init__(self, session_factory: Type[sessionmaker]) -> None:
        assert self.model is not None, "Please set class attribute 'model'"
        self.session_factory = session_factory

    def insert(self, obj: ModelType) -> ModelType:
        with self.session_factory() as db:
            db.add(obj)
            db.commit()
            db.refresh(obj)
        return obj

    def get(self, id: Any) -> Optional[ModelType]:
        with self.session_factory() as db:
            return db.query(self.model).filter(self.model.id == id).scalar()

    def update(self, obj: ModelType) -> ModelType:
        # TODO: Implement update
        raise NotImplementedError()

    def delete(self, id: Any) -> ModelType:
        # TODO: Implement delete
        raise NotImplementedError()


class AccountRepo(AbstractRepo[Account]):
    model = Account

    def get_by_name(self, name: str) -> Optional[Account]:
        with self.session_factory() as db:
            return db.query(self.model).filter(self.model.name == name).scalar()


class EntryRepo(AbstractRepo[Entry]):
    model = Entry


class TransactionRepo(AbstractRepo[Transaction]):
    model = Transaction


account = AccountRepo(SessionLocal)
entry = EntryRepo(SessionLocal)
transaction = TransactionRepo(SessionLocal)
