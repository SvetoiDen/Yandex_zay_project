from aiogram.types import (
    InlineKeyboardButton, InlineKeyboardMarkup,
    ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton, WebAppInfo
)
from data.db_data.db_session import create_session
from data.db_data.models.posts import Posts
from sqlalchemy import func, desc


mainBut = [
    [InlineKeyboardButton(text='Открыть веб сайт',
                          web_app=WebAppInfo(url='https://127.0.0.1:5500/'))],
    [InlineKeyboardButton(text='Создать пост', callback_data='create_web')],
    [InlineKeyboardButton(text='Профиль', callback_data='profile'), InlineKeyboardButton(
        text='Найти пост', callback_data='findPost')]
]
butWeb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Открыть веб сайт', web_app=WebAppInfo(
    url='https://127.0.0.1:5500/form_create'))]], resize_keyboard=True)
mainButShow = InlineKeyboardMarkup(inline_keyboard=mainBut)
postBut = [
    [InlineKeyboardButton(text="❌ Закрыть", callback_data="profile")],
]
postButShow = InlineKeyboardMarkup(inline_keyboard=postBut)


POSTS_PER_PAGE = 5 


async def getUserPostsButtons(user_id: int, page: int = 1) -> InlineKeyboardMarkup:

    db = create_session()
    offset = (page - 1) * POSTS_PER_PAGE

    posts = db.query(Posts).filter(Posts.userId == user_id).order_by(
    desc(Posts.rating)).offset(offset).limit(POSTS_PER_PAGE).all()

    total_posts = db.query(func.count(Posts.id)).filter(
        Posts.userId == user_id).scalar()
    db.close()

    buttons = []
    for post in posts:
        buttons.append([InlineKeyboardButton(
            text=f"{post.namePost} | Лайков: {post.rating}", callback_data=f"open_post_{post.id}")])

    if not buttons:
        buttons.append([InlineKeyboardButton(
            text="У вас пока нет постов", callback_data="no_posts")]) # не обрабатывается

    pagination_buttons = []
    if total_posts > POSTS_PER_PAGE:
        if page > 1:
            pagination_buttons.append(InlineKeyboardButton(
                text="⬅️ Предыдущая", callback_data=f"profile_page_{user_id}_{page - 1}"))
        if offset + POSTS_PER_PAGE < total_posts:
            pagination_buttons.append(InlineKeyboardButton(
                text="Следующая ➡️", callback_data=f"profile_page_{user_id}_{page + 1}"))

    if pagination_buttons:
        buttons.append(pagination_buttons)
    
    buttons.append([InlineKeyboardButton(text="🔙 В меню", callback_data="menu")])

    return InlineKeyboardMarkup(inline_keyboard=buttons)
