from sqlalchemy.orm import Session, joinedload

from database.models import Category


def get_all_category(db: Session) -> Category:
    """Возвращает все категории"""
    return db.query(Category).all()


def get_category(db: Session, category_id: int) -> Category:
    """Получение категории по id"""
    return db.query(Category).filter(Category.id == category_id).first()


def get_films_in_category(db: Session, category_id: int) -> Category:
    """Возвращает все связанные фильмы"""
    category = db.query(
        Category).options(joinedload(Category.films)).get(category_id)
    return category.films if category else []


def add_category(db: Session, name: str):
    """Создание новой категории"""
    new_category = Category(name=name)
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category
