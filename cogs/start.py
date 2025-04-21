from aiogram import Router, Bot, F
from aiogram.types import Message, WebAppData, ContentType, ReplyKeyboardRemove, CallbackQuery
from aiogram.filters.command import Command, CommandStart
from data.db_data.db_session import create_session
from data.db_data.models.users import User
from data.db_data.models.posts import Posts
from data.func.buttons.buttonTg import mainButShow, butWeb
from data.func.functions import codeCreate
from data.config.texts import TEXT_START, TEXT_HTML, TEXT_HTML_2
import logging
import json

start = Router()


@start.message(CommandStart())
async def startCommand(message: Message):
    db = create_session()
    try:
        existing_user = db.query(User).filter(
            User.id == message.from_user.id).first()

        if not existing_user:
            user = User(
                id=message.from_user.id,
                name=message.from_user.username or str(message.from_user.id),
            )
            db.add(user)
            db.commit()
            await message.answer(text=TEXT_START, reply_markup=mainButShow)
        else:
            await message.answer(text="👋 С возвращением!", reply_markup=mainButShow)

    except Exception as e:
        db.rollback()
        logging.error(f"Start command error: {e}")
        await message.answer(text="⚠️ Произошла ошибка при обработке команды")
    finally:
        db.close()

@start.callback_query(F.data == 'create_web')
async def createPost(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer('Нажмите на клавиатуру для создания ссылки', reply_markup=butWeb)

@start.message(F.content_type == ContentType.WEB_APP_DATA)
async def getDataPost(message: Message):
    data = json.loads(message.web_app_data.data)

    idPost = codeCreate()
    db = create_session()
    post = Posts()
    post.id = idPost
    post.userId = message.from_user.id
    post.namePost = data['name']
    post.descPost = data['desc']
    db.add(post)
    db.commit()
    db.close()

    with open(f'templates/posts/{idPost}.html', 'w', encoding='utf-8') as F:
        F.write(TEXT_HTML + '       \n'.join(data['content']) + '\n' + TEXT_HTML_2)

    await message.answer(text=f"Ваш пост успешно создан!", reply_markup=ReplyKeyboardRemove())
