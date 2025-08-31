from aiogram.fsm.state import State, StatesGroup


class FilmStates(StatesGroup):
    main_menu = State()  # Главное меню
    help_window = State()  # Окно помощи

    films_selection = State()  # Выбор фильма
    film_window = State()  # Окно отдельного фильма
    waiting_for_title = State()  # Называния нового фильма
    waiting_for_categories = State()  # Категории для нового фильма
    waiting_for_genres = State()  # Жанр для нового фильма
    waiting_for_description = State()  # Описание для нового фильма

    category_selection = State()  # Выбор категории
    waiting_for_name_category = State()  # Ожидание названия новой категории
    category_window = State()  # Окно отдельной категории

    genre_selection = State()  # Выбор жанра
    genre_window = State()  # Окно жанра
    waiting_for_name_genre = State()  # Ожидание названия жанра

    like_window = State()  # Окно лайков
    admin_window = State()  # Окно админки
