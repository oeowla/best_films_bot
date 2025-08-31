from typing import List

from sqlalchemy import select, exists
from sqlalchemy.ext.asyncio import AsyncSession

from aiogram.types import Message

from database.models import User, Film, user_film
from config import Config


async def get_or_create_user_from_message(
    db: AsyncSession,
    message: Message
) -> User:
    """Создает или возвращает пользователя на основе Telegram сообщения"""
    user = await get_user(db, message.from_user.id)
    if not user:
        user = User(
            telegram_id=message.from_user.id,
            name=message.from_user.full_name,
            is_admin=await is_user_admin(message.from_user.id)
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
    return user


async def is_user_admin(telegram_id: int) -> bool:
    """Проверяет, является ли пользователь админом"""
    admin_ids = [int(x) for x in Config.ADMIN_IDS.split(",")]
    return telegram_id in admin_ids


async def get_user(db: AsyncSession, telegram_id: int) -> User | None:
    """Получает пользователя по ID"""
    result = await db.execute(select(User).where(
        User.telegram_id == telegram_id))
    return result.scalar_one_or_none()


async def get_user_films(db: AsyncSession, telegram_id: int) -> List[Film]:
    """Получает все фильмы юзера"""
    result = await db.execute(
        select(Film)
        .join(user_film, Film.id == user_film.c.film_id)
        .where(user_film.c.user_id == (
            select(User.id).where(
                User.telegram_id == telegram_id).scalar_subquery()
        ))
    )
    return result.scalars().all()


async def check_like_exists(
        db: AsyncSession, telegram_id: int, film_id: int) -> bool:
    """Проверяет, есть ли лайк у пользователя для фильма"""
    stmt = select(user_film).where(
        user_film.c.user_id == (
            select(User.id).where(User.telegram_id == telegram_id)),
        user_film.c.film_id == film_id
    )
    result = await db.execute(stmt)
    return result.scalar_one_or_none() is not None


async def toggle_like(
        db: AsyncSession, telegram_id: int, film_id: int) -> bool:
    user_id_subq = select(
        User.id).where(User.telegram_id == telegram_id).scalar_subquery()

    exists_stmt = select(
        exists().where(
            user_film.c.user_id == user_id_subq,
            user_film.c.film_id == film_id
        )
    )
    is_liked = (await db.execute(exists_stmt)).scalar()

    if is_liked:
        delete_stmt = user_film.delete().where(
            user_film.c.user_id == user_id_subq,
            user_film.c.film_id == film_id
        )
        await db.execute(delete_stmt)
    else:
        insert_stmt = user_film.insert().values(
            user_id=user_id_subq,
            film_id=film_id
        )
        await db.execute(insert_stmt)

    await db.commit()
    return not is_liked
