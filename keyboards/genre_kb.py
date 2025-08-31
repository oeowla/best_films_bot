from typing import List

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.crud.genre import get_all_genre
from database.db import AsyncSessionLocal


async def get_genre_selection_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура выбора жанра фильма"""
    async with AsyncSessionLocal() as db:
        genres = await get_all_genre(db)
    builder = InlineKeyboardBuilder()
    for genre in genres:
        builder.button(
            text=genre.name, callback_data=f'genre_{genre.id}')

    builder.button(text=' 🏠 Главное меню', callback_data='go_to_main')
    builder.button(text=' ⬅️ Назад', callback_data='select_film')

    if genres:
        genre_count = len(genres)
        rows = [3] * (genre_count // 3)

        if remainder := genre_count % 3:
            rows.append(remainder)

        rows.append(2)

        builder.adjust(*rows)
    else:
        builder.adjust(2)

    return builder.as_markup()


async def get_genres_keyboard(
        selected_ids: List[int] = None) -> InlineKeyboardBuilder:
    """Клавиатура с жанрами и отметками выбора (при создании фильма)"""
    if selected_ids is None:
        selected_ids = []

    async with AsyncSessionLocal() as db:
        genres = await get_all_genre(db)
    builder = InlineKeyboardBuilder()

    for genre in genres:
        emoji = '✅' if genre.id in selected_ids else '🔘'
        builder.button(
            text=f'{emoji} {genre.name}',
            callback_data=f'toggle_genre_{genre.id}'
        )
    builder.button(text='⬅️ Назад', callback_data='go_genre_selection')
    builder.button(text='🗸 Готово', callback_data='finish_genres')

    builder.adjust(2, 2)
    return builder.as_markup()
