from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from aiogram.types import Message

from database.models import User
from config import Config



async def get_or_create_user_from_message(
    db: AsyncSession,
    message: Message
) -> User:
    """Создает или возвращает пользователя на основе Telegram сообщения"""
    user = await get_user(db, message.from_user.id)
    if not user:
        user = User(
            user_id=message.from_user.id,
            name=message.from_user.full_name,
            is_admin=await is_user_admin(message.from_user.id)
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
    return user


async def is_user_admin(user_id: int) -> bool:
    """Проверяет, является ли пользователь админом"""
    return user_id in Config.ADMIN_IDS


async def get_user(db: AsyncSession, user_id: int) -> User | None:
    """Получает пользователя по ID"""
    result = await db.execute(select(User).where(User.user_id == user_id))
    return result.scalar_one_or_none()


async def get_user_films(db: AsyncSession, user_id: int) -> list:
    """Получает фильмы пользователя"""
    user = await get_user(db, user_id)
    if not user:
        return []
    
    await db.refresh(user, ['films'])
    return user.films


async def get_user_categories(db: AsyncSession, user_id: int) -> list:
    """Получает категории пользователя"""
    user = await get_user(db, user_id)
    if not user:
        return []
    
    await db.refresh(user, ['categories'])
    return user.categories


async def get_user_genres(db: AsyncSession, user_id: int) -> list:
    """Получает жанры пользователя"""
    user = await get_user(db, user_id)
    if not user:
        return []
    
    await db.refresh(user, ['genres'])
    return user.genres