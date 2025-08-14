from typing import List

from sqlalchemy.orm import Session

from database.models import Film, film_category, film_genre


def get_all_films(db: Session) -> Film:
    """Возвращает все фильмы"""
    return db.query(Film).all()


def get_film_by_id(db: Session, film_id: int) -> Film:
    """Возвращает фильм по id"""
    return db.query(Film).filter(Film.id == film_id).first()


def add_film(
    db: Session, title: str, description: str,
    category_ids: List[int], genre_ids: List[int]
) -> Film:
    """Создание нового фильма"""
    new_film = Film(title=title, description=description)
    db.add(new_film)
    db.flush()

    if category_ids:
        stmt = film_category.insert().values([
            {'film_id': new_film.id, 'category_id': cat_id}
            for cat_id in category_ids
        ])
        db.execute(stmt)

    if genre_ids:
        stmt = film_genre.insert().values([
            {'film_id': new_film.id, 'genre_id': genre_id}
            for genre_id in genre_ids
        ])
        db.execute(stmt)
    db.commit()
    db.refresh(new_film)

    return new_film
