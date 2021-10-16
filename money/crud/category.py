from sqlalchemy.orm.session import Session

from ..models import Category


def create(db: Session, name: str) -> Category:
    category = Category(name=name)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


def get(db: Session, name: str) -> Category:
    return db.query(Category).filter(Category.name == name).scalar()
