from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.crud.user import check_like_exists
from database.crud.category import get_films_in_category
from database.crud.genre import get_films_in_genre
from database.db import AsyncSessionLocal


async def get_film_keyboard(
    back_from: str, back_id: int, film_id: int, telegram_id: int
) -> InlineKeyboardMarkup:
    """Клавиатура для экрана фильма"""
    async with AsyncSessionLocal() as db:
        is_liked = await check_like_exists(db, telegram_id, film_id)

    builder = InlineKeyboardBuilder()

    like_text = '💔 Убрать лайк' if is_liked else '❤️ Лайкнуть фильм'
    builder.button(text=like_text, callback_data=f'toggle_like_{film_id}')

    builder.button(text='🏠 Главное меню', callback_data='go_to_main')

    if back_from == 'genre':
        builder.button(text='⬅️ Назад', callback_data=f'genre_{back_id}')
    elif back_from == 'category':
        builder.button(text='⬅️ Назад', callback_data=f'category_{back_id}')
    elif back_from == 'like':
        builder.button(text='⬅️ Назад', callback_data='my_like')

    builder.adjust(2, 1)
    return builder.as_markup()


async def get_all_films_keyboard(
        id: int, is_genre=False) -> InlineKeyboardMarkup:
    """Клавиатура всех фильмов"""
    async with AsyncSessionLocal() as db:
        if is_genre:
            films = await get_films_in_genre(db, genre_id=id)
        else:
            films = await get_films_in_category(db, category_id=id)

    builder = InlineKeyboardBuilder()

    for film in films:
        builder.button(
            text=film.title,
            callback_data=f'film_{film.id}'
        )
    builder.button(text=' 🏠 Главное меню', callback_data='go_to_main')

    if is_genre:
        builder.button(text=' ⬅️ Назад', callback_data='genres')
    else:
        builder.button(text=' ⬅️ Назад', callback_data='select_film')

    if films:
        film_count = len(films)
        rows = [3] * (film_count // 3)

        if remainder := film_count % 3:
            rows.append(remainder)
        rows.append(2)
        builder.adjust(*rows)
    else:
        builder.adjust(2)

    return builder.as_markup()
