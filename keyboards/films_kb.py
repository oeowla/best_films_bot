from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.crud.category import get_films_in_category
from database.crud.genre import get_films_in_genre
from database.db import get_db


async def get_film_keyboard(
        back_from: str, back_id: int) -> InlineKeyboardMarkup:
    """Клавиатура для экрана фильма"""
    builder = InlineKeyboardBuilder()

    builder.button(text=' 🏠 Главное меню', callback_data='go_to_main')

    if back_from == 'genre':
        builder.button(text=' ⬅️ Назад', callback_data=f'genre_{back_id}')
    elif back_from == 'category':
        builder.button(text=' ⬅️ Назад', callback_data=f'category_{back_id}')

    builder.adjust(2)
    return builder.as_markup()


async def get_all_films_keyboard(
        id: int, is_genre=False) -> InlineKeyboardMarkup:
    """Клавиатура всех фильмов"""
    db = next(get_db())

    if is_genre:
        films = get_films_in_genre(db, genre_id=id)
    else:
        films = get_films_in_category(db, category_id=id)

    builder = InlineKeyboardBuilder()

    for film in films:
        builder.button(
            text=film.title,
            callback_data=f'film_{film.id}'
        )

    builder.button(text=' 🏠 Главное меню', callback_data='go_to_main')

    if is_genre:
        builder.button(text=' ⬅️ Назад', callback_data='go_genres_selection')
    else:
        builder.button(text=' ⬅️ Назад', callback_data='go_catogory_selection')

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
