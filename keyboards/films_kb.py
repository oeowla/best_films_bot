from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)


def get_main_keyboards():
    """Создание стартовой клавиатуры"""
    buttons = [
        [KeyboardButton(text=' 🎬 Выбрать фильм'),
         KeyboardButton(text='❓ Помощь')]
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)


def get_home_keyboard(help=False):
    """Создание постоянной клавиатуры"""
    buttons = [
        [
         KeyboardButton(text='🏠 Домой'),
         ]
    ]
    if help is False:
        buttons.append([KeyboardButton(text='❓ Помощь')])
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)


def get_theme_choice_keyboard():
    """Создание первой инлайн-клавиатуры для выбора тематики"""
    buttons = [
        # Первый ряд
        [
            InlineKeyboardButton(
                text=' 👨‍👩‍👧‍👦 Семейные', callback_data='family'),
            InlineKeyboardButton(
                text=' 💗ྀི C девушкой', callback_data='girlfriend'),
        ],
        # Второй ряд
        [
            InlineKeyboardButton(
                text=' 🤙🏻 С друзьями', callback_data='friends'),
            InlineKeyboardButton(
                text=' 📜🔍 По жанрам', callback_data='genres'),
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
