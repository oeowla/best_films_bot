from aiogram import types, F, Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

from database.db import AsyncSessionLocal
from database.crud.category import get_category
from fsm.states import FilmStates
from keyboards.category_kb import get_category_selection_keyboard
from keyboards.films_kb import get_all_films_keyboard

router = Router()


@router.callback_query(F.data == 'select_film')
async def start_category_selection(callback: CallbackQuery, state: FSMContext):
    """Запуск выбора фильма через категорию"""
    await state.set_state(FilmStates.category_selection)
    await callback.message.edit_text(
        'Выбери категорию фильма:',
        reply_markup=await get_category_selection_keyboard()
    )
    await callback.answer()


@router.callback_query(
    StateFilter(FilmStates.category_selection), F.data.startswith('category_'))
async def choice_category_from_all(
    callback: types.CallbackQuery, state: FSMContext
):
    """Обработка выбора конкретной категории из списка."""
    category_id = int(callback.data.split('_')[1])

    await state.update_data({
        'back_from': 'category',
        'back_id': category_id
    })
    async with AsyncSessionLocal() as db:
        category = await get_category(db, category_id)

    await state.set_state(FilmStates.category_window)
    await callback.message.edit_text(
        f'🎬 Фильмы из категории {category.name}',
        reply_markup=await get_all_films_keyboard(category_id),
        parse_mode="HTML"
    )
    await callback.answer()


@router.callback_query(F.data == 'go_catogory_selection')
async def go_catogory_selection(
    callback: types.CallbackQuery, state: FSMContext
):
    """Возврат к выбору категорий"""
    await state.set_state(FilmStates.category_selection)
    await callback.message.edit_text(
        'Выбери категорию фильма:',
        parse_mode="HTML",
        reply_markup=await get_category_selection_keyboard()
    )
    await callback.answer()


@router.callback_query(F.data.startswith('category_'))
async def choice_category(callback: CallbackQuery, state: FSMContext):
    """Возврат к категории"""
    category_id = int(callback.data.split('_')[1])

    await state.update_data({
        'back_from': 'category',
        'back_id': category_id
    })
    async with AsyncSessionLocal() as db:
        category = await get_category(db, category_id)

    await callback.message.edit_text(
        f'🎬 Фильмы из категории {category.name}',
        reply_markup=await get_all_films_keyboard(category_id),
        parse_mode="HTML"
    )
    await callback.answer()
