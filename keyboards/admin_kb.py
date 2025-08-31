from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


async def get_admin_keyboards() -> InlineKeyboardMarkup:
    """Клавиатура администратора"""
    builder = InlineKeyboardBuilder()

    builder.button(
        text='🎥 Добавить фильм', callback_data='add_film')
    builder.button(
        text='🎥 Создать категорию', callback_data='create_category')
    builder.button(
        text='🎥 Создать жанр', callback_data='create_genre')
    builder.button(
        text=' 🏠 Главное меню', callback_data='go_to_main')

    builder.adjust(3, 1)
    return builder.as_markup()
