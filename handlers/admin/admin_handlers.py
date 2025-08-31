from aiogram import Router, types, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from fsm.states import FilmStates
from keyboards.admin_kb import get_admin_keyboards

router = Router()


@router.callback_query(
    StateFilter(FilmStates.like_window), F.data == 'admin')
async def admin(callback: types.CallbackQuery, state: FSMContext):
    """админка"""
    await callback.message.edit_text(
        'Все будет хорошо - главное верить',
        reply_markup=await get_admin_keyboards()
    )
    await state.set_state(FilmStates.admin_window)
