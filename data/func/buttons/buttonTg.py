from aiogram.types import (
    InlineKeyboardButton, InlineKeyboardMarkup,
    ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton, WebAppInfo
)
from data.db_data.db_session import create_session
from data.db_data.models.posts import Posts

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


async def getUserPostsButtons(user_id: int) -> InlineKeyboardMarkup:

    db = create_session()
    posts = db.query(Posts).filter(Posts.userId == user_id).all()
    db.close()

    buttons = []
    for post in posts:
        buttons.append([InlineKeyboardButton(
            text=f"{post.namePost} | Лайков: {post.rating}", callback_data=f"open_post_{post.id}")])

    if not buttons:
        buttons.append([InlineKeyboardButton(
            text="У вас пока нет постов", callback_data="no_posts")])

    return InlineKeyboardMarkup(inline_keyboard=buttons)
