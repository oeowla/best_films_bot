from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.crud.user import get_user_films


async def get_all_like_keyboard(db, user) -> InlineKeyboardMarkup:
    """Клавиатура всех лайков"""
    films = await get_user_films(db=db, telegram_id=user.telegram_id)
    builder = InlineKeyboardBuilder()
    for film in films:
        builder.button(
            text=film.title,
            callback_data=f'film_{film.id}'
        )

    rows = []

    if films:
        film_count = len(films)
        rows = [3] * (film_count // 3)

        if remainder := film_count % 3:
            rows.append(remainder)
    builder.button(text=' 🏠 Главное меню', callback_data='go_to_main')
    if user.is_admin:
        builder.button(
            text='админка', callback_data='admin')
        rows.append(2) if films else builder.adjust(2)
    else:
        rows.append(1) if films else builder.adjust(1)

    if films:
        builder.adjust(*rows)

    return builder.as_markup()
