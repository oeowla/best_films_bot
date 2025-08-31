from aiogram import Router, types, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from database.db import AsyncSessionLocal
from database.crud.genre import add_genre
from fsm.states import FilmStates

router = Router()


@router.callback_query(
    StateFilter(FilmStates.admin_window), F.data == 'create_genre')
async def new_genre(callback: types.CallbackQuery, state: FSMContext):
    """Инициализация процесса добавления нового жанра."""
    await callback.message.edit_text(
        'Введите название жанра', parse_mode="HTML"
    )
    await state.set_state(FilmStates.waiting_for_name_genre)


@router.message(StateFilter(FilmStates.waiting_for_name_genre))
async def process_genre_name(message: types.Message, state: FSMContext):
    """Сохранение категории в БД"""
    name = message.text
    async with AsyncSessionLocal() as db:
        await add_genre(db, name=name)
    await message.answer(f'Жанр {name} успешно добавлен')
    await state.clear()
