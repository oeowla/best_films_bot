from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import Config
from .models import Base

# Создаем 'движок' - основной интерфейс к базе данных
# echo=True - будет показывать SQL-запросы в консоли (удобно для отладки)
engine = create_engine(
    Config.DATABASE_URL, connect_args={"check_same_thread": False}, echo=True
)
# SessionLocal - это фабрика для создания сессий БД
# autocommit=False - изменения не применяются автоматически
# autoflush=False - не отправляем запросы без необходимости
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


def init_db():
    # Создаёт все таблицы
    Base.metadata.create_all(bind=engine)


def get_db():
    """Генератор сессий для DI"""
    db = SessionLocal()
    try:
        yield db  # Отдаем сессию для использования
    finally:
        db.close()  # Закрываем сессию в любом случае
