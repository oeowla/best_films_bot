from aiogram import Router, types, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext

from fsm.states import FilmStates

from keyboards.base_kb import get_main_keyboards, help_keyboard

router = Router()


@router.message(Command('start'))
async def main_command(message: types.Message, state: FSMContext):
    """Обработка команды /start - главное меню."""
    await message.answer(
        '👋 Привет! Я бот для поиска фильмов.\nВыбери действие:',
        reply_markup=await get_main_keyboards()
    )
    await state.set_state(FilmStates.main_menu)


@router.callback_query(
    StateFilter(FilmStates.main_menu), F.data == 'help')
async def help_command(callback: types.CallbackQuery, state: FSMContext):
    """Показ справки по работе с ботом."""
    await callback.message.edit_text(
        'Здесь будет помощь',
        parse_mode="HTML",
        reply_markup=await help_keyboard()
    )
    await state.set_state(FilmStates.help_window)
