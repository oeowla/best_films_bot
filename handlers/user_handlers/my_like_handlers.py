from aiogram import F, Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

from database.db import AsyncSessionLocal
from database.crud.user import get_user, toggle_like
from fsm.states import FilmStates
from keyboards.user_kb import get_all_like_keyboard
from keyboards.films_kb import get_film_keyboard

router = Router()


@router.callback_query(F.data == 'my_like')
async def start_category_selection(callback: CallbackQuery, state: FSMContext):
    """Окно лайков"""
    async with AsyncSessionLocal() as db:
        user = await get_user(db, callback.from_user.id)
    await state.set_state(FilmStates.like_window)
    await callback.message.edit_text(
        'вот все, что ты лайкал:',
        reply_markup=await get_all_like_keyboard(db=db, user=user)
    )


@router.callback_query(F.data.startswith('toggle_like_'))
async def handle_like_toggle(
    callback: CallbackQuery, state: FSMContext
):
    film_id = int(callback.data.split('_')[-1])
    telegram_id = callback.from_user.id
    await state.update_data({
        'back_from': 'like',
    })
    async with AsyncSessionLocal() as db:
        await toggle_like(db, telegram_id, film_id)

    # Получаем текущее состояние из FSM
    data = await state.get_data()

    # Обновляем клавиатуру
    await callback.message.edit_reply_markup(
        reply_markup=await get_film_keyboard(
            back_from=data.get('back_from'),
            back_id=data.get('back_id'),
            film_id=film_id,
            telegram_id=telegram_id,
        )
    )
    await callback.answer()
