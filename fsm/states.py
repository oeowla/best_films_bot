from aiogram.fsm.state import State, StatesGroup


class FilmStates(StatesGroup):
    waiting_for_action = State()  # Ожидание выбора действия
    waiting_for_category = State()  # Ожидание категории
    waiting_for_films = State()  # Ожидание выбора фильма
