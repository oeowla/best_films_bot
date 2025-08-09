import asyncio

from aiogram import Bot, Dispatcher, types, F
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command

from config import config
from handlers.films_handlers import (
    start_command,
    go_home,
    help_command,
    process_action_selection
)


async def main():
    """Функция запуска бота"""
    # Инициализация бота и диспетчера
    bot = Bot(token=config.BOT_TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher(storage=MemoryStorage())

    # Регистрация обработчиков сообщений и команд
    dp.message.register(start_command, Command('start'))
    dp.message.register(go_home, F.text == '🏠 Домой')
    dp.message.register(help_command, F.text == '❓ Помощь')
    dp.message.register(process_action_selection, F.text == '🎬 Выбрать фильм')

    # Установка команд меню бота
    await bot.set_my_commands([
        types.BotCommand(command='start', description='Начать работу')
    ])
    try:
        # Запуск бота в режиме опроса сервера telegram
        print('Бот успешно запущен!')
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(main())
