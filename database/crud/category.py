from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select

from database.models import Category


async def get_all_category(db: AsyncSession) -> list[Category]:
    """Возвращает все категории"""
    result = await db.execute(select(Category))
    return result.scalars().all()


async def get_category(db: AsyncSession, category_id: int) -> Category | None:
    """Получение категории по id"""
    result = await db.execute(select(Category).where(
        Category.id == category_id))
    return result.scalar_one_or_none()


async def get_films_in_category(db: AsyncSession, category_id: int) -> list:
    """Возвращает все связанные фильмы"""
    result = await db.execute(
        select(Category)
        .where(Category.id == category_id)
        .options(selectinload(Category.films))
    )
    category = result.scalar_one_or_none()
    return category.films if category else []


async def add_category(db: AsyncSession, name: str) -> Category:
    """Создание новой категории"""
    new_category = Category(name=name)
    db.add(new_category)
    await db.commit()
    await db.refresh(new_category)
    return new_category
