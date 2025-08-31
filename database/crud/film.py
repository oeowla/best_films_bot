from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert

from database.models import Film, film_category, film_genre


async def get_all_films(db: AsyncSession) -> list[Film]:
    """Возвращает все фильмы"""
    result = await db.execute(select(Film))
    return result.scalars().all()


async def get_film_by_id(db: AsyncSession, film_id: int) -> Film | None:
    """Возвращает фильм по id"""
    result = await db.execute(select(Film).where(Film.id == film_id))
    return result.scalar_one_or_none()


async def add_film(
    db: AsyncSession,
    title: str,
    description: str,
    category_ids: list[int],
    genre_ids: list[int]
) -> Film:
    """Создание нового фильма"""
    new_film = Film(title=title, description=description)
    db.add(new_film)
    await db.flush()

    if category_ids:
        await db.execute(
            insert(film_category),
            [{'film_id': new_film.id, 'category_id': cat_id
              } for cat_id in category_ids]
        )

    if genre_ids:
        await db.execute(
            insert(film_genre),
            [{'film_id': new_film.id, 'genre_id': genre_id
              } for genre_id in genre_ids]
        )

    await db.commit()
    await db.refresh(new_film)
    return new_film
