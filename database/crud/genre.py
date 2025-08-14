from sqlalchemy.orm import Session, joinedload

from database.models import Genre


def get_all_genre(db: Session) -> Genre:
    """Возвращает все жанры"""
    return db.query(Genre).all()


def get_genre(db: Session, genre_id: int) -> Genre:
    """Получение жанра по id"""
    return db.query(Genre).filter(Genre.id == genre_id).first()


def get_films_in_genre(db: Session, genre_id: int) -> Genre:
    """Возвращает все связанные фильмы"""
    genre = db.query(
        Genre).options(joinedload(Genre.films)).get(genre_id)
    return genre.films if genre else []


def add_genre(db: Session, name: str):
    """Создание нового жанра"""
    new_genre = Genre(name=name)
    db.add(new_genre)
    db.commit()
    db.refresh(new_genre)
    return new_genre
