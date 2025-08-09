from aiogram import types
from aiogram.fsm.context import FSMContext

from fsm.states import FilmStates
from keyboards.films_kb import (
    get_main_keyboards,
    get_theme_choice_keyboard,
    get_home_keyboard
)


async def start_command(message: types.Message):
    """Стартовая команда"""
    await message.answer(
        '👋 Привет! Я бот для поиска фильмов.\nВыбери действие:',
        reply_markup=get_main_keyboards()
    )


async def go_home(message: types.Message, state: FSMContext):
    """Обработка кнопки 'Домой'"""
    await message.answer(
        'Давай выберем новый фильм',
        reply_markup=get_main_keyboards()
    )


async def help_command(message: types.Message):
    """Обработка кнопки 'Помощь'"""
    await message.answer(
        'j',
        reply_markup=get_home_keyboard(help=True)
    )


async def process_action_selection(message: types.Message, state: FSMContext):
    """Обработчик запроса на выбор фильма. При кнопке 'Выбрать фильм'"""
    await state.set_state(FilmStates.waiting_for_category)
    await state.update_data(action='film')
    await message.answer(
        'Выбери категорию фильма:', reply_markup=get_theme_choice_keyboard()
    )
