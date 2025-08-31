from aiogram import types, F, Router
from aiogram.fsm.context import FSMContext

from fsm.states import FilmStates
from keyboards.genre_kb import get_genre_selection_keyboard
from keyboards.films_kb import get_all_films_keyboard
from database.db import AsyncSessionLocal
from database.crud.genre import get_genre
router = Router()


@router.callback_query(F.data == 'genres')
async def choosing_film_by_genre(
    callback: types.CallbackQuery, state: FSMContext
):
    """Запуск выбора фильма через жанры."""
    await state.set_state(FilmStates.genre_selection)
    await callback.message.edit_text(
        '🎭 Выберите жанр:',
        reply_markup=await get_genre_selection_keyboard()
    )
    await callback.answer()


@router.callback_query(F.data.startswith('genre_'))
async def choice_genre_from_all(
    callback: types.CallbackQuery, state: FSMContext
):
    """Обработка выбора конкретного жанра из списка."""
    genre_id = int(callback.data.split('_')[1])

    await state.update_data({
        'back_from': 'genre',
        'back_id': genre_id
    })
    async with AsyncSessionLocal() as db:
        genre = await get_genre(db, genre_id)

    await state.set_state(FilmStates.genre_window)
    await callback.message.edit_text(
        f'🎬 Фильмы из жанра {genre.name}',
        reply_markup=await get_all_films_keyboard(genre_id, is_genre=True),
        parse_mode="HTML"
    )
    await callback.answer()
