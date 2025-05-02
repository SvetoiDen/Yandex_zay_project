import base64
from aiogram import Router, Bot, F
from aiogram.types import Message, WebAppData, ContentType, ReplyKeyboardRemove, CallbackQuery
from aiogram.filters.command import Command, CommandStart
from data.db_data.db_session import create_session
from data.db_data.models.users import User
from data.db_data.models.posts import Posts
from data.db_data.models.admins import Admin
from data.db_data.models.images import ImagePosts
from data.func.buttons.buttonTg import mainButShow, butWeb
from data.func.functions import codeCreate
from data.config.texts import TEXT_START, TEXT_HTML, TEXT_HTML_2
import logging
import json

start = Router()
DEFAULT_ADMIN_ID = [1012085977, 1099501680]


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

        for admin_id in DEFAULT_ADMIN_ID:
            existing_admin = db.query(Admin).filter(
                Admin.user_id == admin_id).first()
            if not existing_admin:
                new_admin = Admin(user_id=admin_id, level=3)
                db.add(new_admin)

        db.commit()
        await message.answer(text=TEXT_START, reply_markup=mainButShow)


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
    dataContent = data['content']
    print(dataContent)

    db = create_session()
    post = Posts()
    post.id = data['id']
    post.userId = message.from_user.id
    post.namePost = data['name']
    post.descPost = data['desc']
    db.add(post)
    db.commit()

    newContent = []
    i = 0
    for elem in dataContent:
        if elem.startswith('img'):
            typeImg = elem.split('_')[-1]
            newTypeImg = "data:" + typeImg + ";base64,"
            image = db.query(ImagePosts).filter(ImagePosts.post_id == data['id'], ImagePosts.pos == i).first()
            newTypeImg = "data:" + typeImg + f";base64,{str(image.image)[2:-1]}"
            newContent.append(f"<img src='{newTypeImg}' />")
            i = i + 1
        else:
            newContent.append(elem)
    db.close()

    with open(f'templates/posts/{data['id']}.html', 'w', encoding='utf-8') as F:
        F.write(TEXT_HTML + '\n'.join(newContent) + '\n' + TEXT_HTML_2)

    await message.answer(text=f"Ваш пост успешно создан!", reply_markup=ReplyKeyboardRemove())


@start.callback_query(F.data == 'menu')
async def return_to_menu(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer(TEXT_START, reply_markup=mainButShow)


@start.message(F.text == '❌ Отмена')
async def close_create_post(message: Message):
    await message.delete()
    await message.bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
