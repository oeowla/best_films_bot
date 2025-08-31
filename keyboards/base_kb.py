from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


async def get_main_keyboards() -> InlineKeyboardMarkup:
    """Клавиатура главного меню"""
    builder = InlineKeyboardBuilder()

    builder.button(
        text='🎬 Выбрать фильм', callback_data='select_film')
    builder.button(
        text='𓆩❤︎𓆪 Мои лайки', callback_data='my_like')
    builder.button(
        text='❓ Помощь', callback_data='help')

    builder.adjust(1, 2)
    return builder.as_markup()


async def help_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура окна 'помощь'"""
    builder = InlineKeyboardBuilder()

    builder.button(text=' ⬅️ Назад', callback_data='go_to_main')

    return builder.as_markup()
