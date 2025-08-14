from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


async def get_main_keyboards() -> InlineKeyboardMarkup:
    """Клавиатура главного меню"""
    builder = InlineKeyboardBuilder()

    builder.button(
        text=' 🎥 Добавить фильм', callback_data='add_film')
    builder.button(
        text=' 🎥 Создать категорию', callback_data='create_category')
    builder.button(
        text=' 🎥 Создать жанр', callback_data='create_genre')
    builder.button(
        text=' 🎬 Выбрать фильм', callback_data='select_film')
    builder.button(
        text='❓ Помощь', callback_data='help')

    builder.adjust(3, 2)
    return builder.as_markup()


async def help_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура окна 'помощь'"""
    builder = InlineKeyboardBuilder()

    builder.button(text=' ⬅️ Назад', callback_data='go_to_main')

    return builder.as_markup()
