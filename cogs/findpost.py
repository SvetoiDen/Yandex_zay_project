from sqlalchemy import desc
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram import Router, F
import logging
from data.func.functions import findPost
from aiogram.types import CallbackQuery, Message
from data.db_data.db_session import create_session
from data.db_data.models.users import User
from data.db_data.models.posts import Posts
from data.func.buttons.buttonTg import postButShow
from aiogram.fsm.context import FSMContext
from data.func.states import SearchStates


finder = Router()


@finder.callback_query(F.data == "findPost")
async def find_post_callback(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer("🔎 Введите текст для поиска постов:")
    await state.set_state(SearchStates.waiting_for_query)
    await callback.answer()


POSTS_PER_PAGE = 5


@finder.message(SearchStates.waiting_for_query)
async def process_search(message: Message, state: FSMContext):
    query = message.text
    await state.update_data(query=query, page=1)

    await show_search_results(message, state)


async def show_search_results(message_or_callback, state: FSMContext):
    data = await state.get_data()
    query = data['query']
    page = data.get('page', 1)

    db = create_session()
    posts = db.query(Posts).filter(
        (Posts.namePost.ilike(f'%{query}%')) |
        (Posts.descPost.ilike(f'%{query}%'))
    ).order_by(desc(Posts.rating)).offset((page - 1) * POSTS_PER_PAGE).limit(POSTS_PER_PAGE).all()

    total = db.query(Posts).filter(
        (Posts.namePost.ilike(f'%{query}%')) |
        (Posts.descPost.ilike(f'%{query}%'))
    ).count()
    db.close()

    if not posts:
        await message_or_callback.answer("❌ Посты не найдены.")
        await state.clear()
        return

    buttons = [[InlineKeyboardButton(
        text=f"{post.namePost} | ⭐ {post.rating}",
        callback_data=f"open_post_{post.id}"
    )] for post in posts]

    pagination_buttons = []
    if page > 1:
        pagination_buttons.append(InlineKeyboardButton(
            text="⬅️ Назад", callback_data=f"search_page_{page - 1}"))
    if page * POSTS_PER_PAGE < total:
        pagination_buttons.append(InlineKeyboardButton(
            text="Вперед ➡️", callback_data=f"search_page_{page + 1}"))
    if pagination_buttons:
        buttons.append(pagination_buttons)

    buttons.append([InlineKeyboardButton(
        text="🔙 В меню", callback_data="menu")])

    await message_or_callback.answer(
        "🔍 Найденные посты:",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons)
    )


@finder.callback_query(F.data.startswith("search_page_"))
async def search_page_callback(callback: CallbackQuery, state: FSMContext):
    page = int(callback.data.split("_")[-1])
    await state.update_data(page=page)

    await callback.message.delete()
    await show_search_results(callback.message, state)
    await callback.answer()
