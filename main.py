import asyncio

from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from database.db import init_db
from config import config
from handlers import (
    base_handlers, films_handlers, category_handlers, genre_handlers
)
from handlers.admin import (
    create_category_handlers, create_film_handlers,
    create_genre_handlers, admin_handlers
)
from handlers.user_handlers import my_like_handlers


async def main():
    """Функция запуска бота"""
    await init_db()
    # Инициализация бота и диспетчера
    bot = Bot(token=config.BOT_TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher(storage=MemoryStorage())

    # Подключение роутеров
    dp.include_router(base_handlers.router)
    dp.include_router(films_handlers.router)
    dp.include_router(category_handlers.router)
    dp.include_router(genre_handlers.router)
    dp.include_router(create_film_handlers.router)
    dp.include_router(create_category_handlers.router)
    dp.include_router(create_genre_handlers.router)
    dp.include_router(admin_handlers.router)
    dp.include_router(my_like_handlers.router)

    # Установка команд меню бота
    await bot.set_my_commands([
        types.BotCommand(command='start', description='Начать работу')
    ])
    dp
    try:
        # Запуск бота в режиме опроса сервера telegram
        print('Бот успешно запущен!')
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(main())
