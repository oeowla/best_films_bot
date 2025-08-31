from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from fsm.states import FilmStates

from keyboards.base_kb import get_main_keyboards, help_keyboard
from database.db import AsyncSessionLocal
from database.crud.user import get_or_create_user_from_message

router = Router()


@router.message(Command('start'))
async def main_command(message: types.Message, state: FSMContext):
    """Обработка команды /start - главное меню."""
    async with AsyncSessionLocal() as db:
        user = await get_or_create_user_from_message(db=db, message=message)
    await message.answer(
        f'👋 Привет, {user.name}! Я бот для поиска фильмов.\nВыбери действие:',
        reply_markup=await get_main_keyboards()
    )
    await state.set_state(FilmStates.main_menu)


@router.callback_query(F.data == 'help')
async def help_command(callback: types.CallbackQuery, state: FSMContext):
    """Показ справки по работе с ботом."""
    help_text = """
    🎬 <b>Помощь по использованию ботом</b>

    Здесь ты можешь:
    • <b>Выбирать фильмы</b> - через категории или жанры
    • <b>Ставить лайки</b> ❤️ - сохранять понравившиеся фильмы
    • <b>Просматривать</b> свои лайки в разделе "Мои лайки"

    <b>Как пользоваться:</b>
    1. Нажми "Выбрать фильм"
    2. Выбери категорию или перейди к выбору по жанрам
    3. Листай список фильмов и выбирай понравившийся
    4. На странице фильма можешь поставить лайк или вернуться назад
    """
    await callback.message.edit_text(
        help_text,
        parse_mode="HTML",
        reply_markup=await help_keyboard()
    )
    await state.set_state(FilmStates.help_window)
