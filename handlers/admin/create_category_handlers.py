from aiogram import Router, types, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from database.db import AsyncSessionLocal
from database.crud.category import add_category
from fsm.states import FilmStates

router = Router()


@router.callback_query(
    StateFilter(FilmStates.admin_window), F.data == 'create_category')
async def new_category(callback: types.CallbackQuery, state: FSMContext):
    """Инициализация процесса добавления новой категории."""
    await callback.message.edit_text(
        'Введите название категории', parse_mode="HTML"
    )
    await state.set_state(FilmStates.waiting_for_name_category)


@router.message(StateFilter(FilmStates.waiting_for_name_category))
async def process_category_name(message: types.Message, state: FSMContext):
    """Сохранение категории в БД"""
    name = message.text
    async with AsyncSessionLocal() as db:
        await add_category(db, name=name)
    await message.answer(f'Категория {name} успешно добавлена')
    await state.clear()
