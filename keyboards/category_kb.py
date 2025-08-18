from typing import List

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.crud.category import get_all_category
from database.db import AsyncSessionLocal


async def get_category_selection_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура выбора категории фильма"""
    async with AsyncSessionLocal() as db:
        categories = await get_all_category(db)
    builder = InlineKeyboardBuilder()
    for category in categories:
        builder.button(
            text=category.name, callback_data=f'category_{category.id}')

    builder.button(text=' 📜🔍 По жанрам', callback_data='genres')
    builder.button(text=' ⬅️ Назад', callback_data='go_to_main')

    if categories:
        category_count = len(categories)
        rows = [3] * (category_count // 3)

        if remainder := category_count % 3:
            rows.append(remainder)

        rows.append(2)

        builder.adjust(*rows)
    else:
        builder.adjust(2)

    return builder.as_markup()


async def get_categories_keyboard(
        selected_ids: List[int] = None) -> InlineKeyboardBuilder:
    """Клавиатура с категориями и отметками выбора (при создании фильма)"""
    if selected_ids is None:
        selected_ids = []

    async with AsyncSessionLocal() as db:
        categories = await get_all_category(db)
    builder = InlineKeyboardBuilder()

    for category in categories:
        emoji = '✅' if category.id in selected_ids else '🔘'
        builder.button(
            text=f'{emoji} {category.name}',
            callback_data=f'toggle_category_{category.id}'
        )

    builder.button(text='⬅️ Назад', callback_data='go_category_selection')
    builder.button(text='🗸 Готово', callback_data='finish_categories')

    builder.adjust(2, 2)
    return builder.as_markup()
