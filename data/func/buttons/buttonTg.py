from aiogram.types import (
    InlineKeyboardButton, InlineKeyboardMarkup,
    ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton, WebAppInfo
)

mainBut = [
    [InlineKeyboardButton(text='Открыть веб сайт', web_app=WebAppInfo(url='https://127.0.0.1:5500/'))],
    [InlineKeyboardButton(text='Создать пост', callback_data='create_web')],
    [InlineKeyboardButton(text='Профиль', callback_data='profile'), InlineKeyboardButton(text='Найти пост', callback_data='findPost')]
]
butWeb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Открыть веб сайт', web_app=WebAppInfo(url='https://127.0.0.1:5500/form_create'))]], resize_keyboard=True)
mainButShow = InlineKeyboardMarkup(inline_keyboard=mainBut)