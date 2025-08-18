from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select

from database.models import Genre


async def get_all_genre(db: AsyncSession) -> list[Genre]:
    """Возвращает все жанры"""
    result = await db.execute(select(Genre))
    return result.scalars().all()


async def get_genre(db: AsyncSession, genre_id: int) -> Genre | None:
    """Получение жанра по id"""
    result = await db.execute(select(Genre).where(Genre.id == genre_id))
    return result.scalar_one_or_none()


async def get_films_in_genre(db: AsyncSession, genre_id: int) -> list:
    """Возвращает все связанные фильмы"""
    result = await db.execute(
        select(Genre)
        .where(Genre.id == genre_id)
        .options(selectinload(Genre.films))
    )
    genre = result.scalar_one_or_none()
    return genre.films if genre else []


async def add_genre(db: AsyncSession, name: str) -> Genre:
    """Создание нового жанра"""
    new_genre = Genre(name=name)
    db.add(new_genre)
    await db.commit()
    await db.refresh(new_genre)
    return new_genre
