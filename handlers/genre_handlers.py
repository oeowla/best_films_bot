from aiogram import types, F, Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

from fsm.states import FilmStates
from keyboards.genre_kb import get_genre_selection_keyboard
from keyboards.films_kb import get_all_films_keyboard
from database.db import get_db
from database.crud.genre import get_genre
router = Router()


@router.callback_query(
    StateFilter(FilmStates.category_selection), F.data == 'genres')
async def choosing_film_by_genre(
    callback: types.CallbackQuery, state: FSMContext
):
    """Запуск выбора фильма через жанры."""
    await state.set_state(FilmStates.genre_selection)
    await callback.message.edit_text(
        '🎭 Выберите жанр:',
        parse_mode="HTML",
        reply_markup=await get_genre_selection_keyboard()
    )
    await callback.answer()


@router.callback_query(
    StateFilter(FilmStates.genre_selection), F.data.startswith('genre_')
)
async def choice_genre_from_all(
    callback: types.CallbackQuery, state: FSMContext
):
    """Обработка выбора конкретного жанра из списка."""
    genre_id = int(callback.data.split('_')[1])
    db = next(get_db())

    await state.update_data({
        'back_from': 'genre',
        'back_id': genre_id
    })

    genre = get_genre(db, genre_id)

    await state.set_state(FilmStates.genre_window)
    await callback.message.edit_text(
        f'🎬 Фильмы из жанра {genre.name}',
        reply_markup=await get_all_films_keyboard(genre_id, is_genre=True),
        parse_mode="HTML"
    )
    await callback.answer()


@router.callback_query(F.data == 'go_genres_selection')
async def go_genre_selection(
    callback: types.CallbackQuery, state: FSMContext
):
    """Возврат к выбору жанра"""
    await state.set_state(FilmStates.genre_selection)
    await callback.message.edit_text(
        'Выбери жанр фильма:',
        parse_mode="HTML",
        reply_markup=await get_genre_selection_keyboard()
    )
    await callback.answer()


@router.callback_query(F.data.startswith('genre_'))
async def choice_genre(callback: CallbackQuery, state: FSMContext):
    """Возврат к жанру"""
    genre_id = int(callback.data.split('_')[1])
    db = next(get_db())

    await state.update_data({
        'back_from': 'genre',
        'back_id': genre_id
    })

    genre = get_genre(db, genre_id)

    await state.set_state(FilmStates.genre_window)
    await callback.message.edit_text(
        f'🎬 Фильмы из жанра {genre.name}',
        reply_markup=await get_all_films_keyboard(genre_id, is_genre=True),
        parse_mode="HTML"
    )
    await callback.answer()

