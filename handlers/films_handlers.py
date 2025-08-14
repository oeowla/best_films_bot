from aiogram import types, F, Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext


from fsm.states import FilmStates
from database.db import get_db
from database.crud.film import get_film_by_id

from keyboards.base_kb import get_main_keyboards
from keyboards.films_kb import get_film_keyboard

router = Router()


@router.callback_query(F.data.startswith('film_'))
async def show_film(
    callback: CallbackQuery,
    state: FSMContext
):
    """Окно фильма"""
    film_id = int(callback.data.split('_')[1])
    db = next(get_db())
    film = get_film_by_id(db, film_id)

    categories = ", ".join([c.name for c in film.categories])
    genres = ", ".join([g.name for g in film.genres])

    text = (
        f"🎬 <b>{film.title}</b>\n\n"
        f"📝 <i>{film.description}</i>\n\n"
        f"📂 Категории: {categories}\n"
        f"🏷️ Жанры: {genres}"
    )

    state_data = await state.get_data()
    keyboard = await get_film_keyboard(
        back_from=state_data.get('back_from'),
        back_id=state_data.get('back_id')
    )

    await callback.message.edit_text(
        text,
        reply_markup=keyboard,
        parse_mode="HTML"
    )
    await callback.answer()


@router.callback_query(F.data == 'go_to_main')
async def go_back_to_main(callback: types.CallbackQuery, state: FSMContext):
    """Возврат в главное меню"""
    await state.set_state(FilmStates.main_menu)
    await callback.message.edit_text(
        '👋 Привет! Я бот для поиска фильмов.\nВыбери действие:',
        reply_markup=await get_main_keyboards()
    )
    await callback.answer()
