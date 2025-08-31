from typing import List

from aiogram import Router, types, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from database.db import AsyncSessionLocal
from database.crud.film import add_film
from fsm.states import FilmStates
from keyboards.category_kb import get_categories_keyboard
from keyboards.genre_kb import get_genres_keyboard

router = Router()


@router.callback_query(
    StateFilter(FilmStates.admin_window), F.data == 'add_film')
async def new_film(callback: types.CallbackQuery, state: FSMContext):
    """Начало добавления нового фильма"""
    await callback.message.edit_text(
        'Введите название фильма', parse_mode="HTML"
    )
    await state.set_state(FilmStates.waiting_for_title)
    await state.update_data(
        selected_categories=[],
        selected_genres=[]
    )


@router.message(StateFilter(FilmStates.waiting_for_title))
async def process_film_title(message: types.Message, state: FSMContext):
    """Обработка названия фильма и вывод клавиатуры категорий"""
    await state.update_data(title=message.text)
    await message.answer(
        'Выберите категории фильма (можно несколько):',
        reply_markup=await get_categories_keyboard()
    )
    await state.set_state(FilmStates.waiting_for_categories)


@router.callback_query(
    StateFilter(FilmStates.waiting_for_categories),
    F.data.startswith('toggle_category_')
)
async def toggle_category(callback: types.CallbackQuery, state: FSMContext):
    """Переключение состояния выбранной категории"""
    data = await state.get_data()
    selected_ids: List[int] = data.get('selected_categories', [])
    category_id = int(callback.data.split("_")[-1])

    if category_id in selected_ids:
        selected_ids.remove(category_id)
    else:
        selected_ids.append(category_id)

    await state.update_data(selected_categories=selected_ids)
    await callback.message.edit_reply_markup(
        reply_markup=await get_categories_keyboard(selected_ids)
    )
    await callback.answer()


@router.callback_query(
    StateFilter(FilmStates.waiting_for_categories),
    F.data == 'finish_categories'
)
async def finish_categories(callback: types.CallbackQuery, state: FSMContext):
    """Завершение выбора категорий и переход к выбору жанров"""
    await callback.message.edit_text(
        'Теперь выберите жанры фильма (можно несколько):',
        reply_markup=await get_genres_keyboard()
    )
    await state.set_state(FilmStates.waiting_for_genres)


@router.callback_query(
    StateFilter(FilmStates.waiting_for_genres),
    F.data.startswith('toggle_genre_')
)
async def toggle_genre(callback: types.CallbackQuery, state: FSMContext):
    """Переключение состояния выбранного жанра"""
    data = await state.get_data()
    selected_ids: List[int] = data.get('selected_genres', [])
    genre_id = int(callback.data.split("_")[-1])

    if genre_id in selected_ids:
        selected_ids.remove(genre_id)
    else:
        selected_ids.append(genre_id)

    await state.update_data(selected_genres=selected_ids)
    await callback.message.edit_reply_markup(
        reply_markup=await get_genres_keyboard(selected_ids)
    )
    await callback.answer()


@router.callback_query(
    StateFilter(FilmStates.waiting_for_genres),
    F.data == 'finish_genres'
)
async def finish_genres(callback: types.CallbackQuery, state: FSMContext):
    """Завершение выбора жанров и запрос описания"""
    await callback.message.edit_text('Теперь введите описание фильма')
    await state.set_state(FilmStates.waiting_for_description)


@router.message(StateFilter(FilmStates.waiting_for_description))
async def process_film_description(message: types.Message, state: FSMContext):
    """Сохранение фильма с выбранными категориями и жанрами"""
    data = await state.get_data()
    async with AsyncSessionLocal() as db:
        await add_film(
            db,
            title=data['title'],
            description=message.text,
            category_ids=data['selected_categories'],
            genre_ids=data['selected_genres']
        )
    await message.answer(f'Фильм {data["title"]} успешно добавлен!')
    await state.clear()
