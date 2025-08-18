from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from config import Config
from .models import Base

# Создаем асинхронный движок для SQLite
engine = create_async_engine(Config.DATABASE_URL, echo=True)

# Создаем фабрику асинхронных сессий
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)


async def init_db():
    """Создает все таблицы в базе данных"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Корректный асинхронный генератор сессий для DI"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
