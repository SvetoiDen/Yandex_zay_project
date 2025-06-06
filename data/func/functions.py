import datetime
import logging
import os
from sqlalchemy.ext.asyncio import AsyncSession
import string
import random
import asyncio
import traceback
from aiogram.types import User, UserProfilePhotos
from aiogram import Bot
from aiogram.methods import GetUserProfilePhotos
from data.db_data.db_session import create_session
from data.db_data.models.users import User
from data.db_data.models.images import ImagePosts
from data.db_data.models.posts import Posts
from data.db_data.models.admins import Admin
from data.db_data.models.comments import Comment
from sqlalchemy.orm import Session
import requests
import io
from PIL import Image, ImageDraw, ImageFont


def codeCreate():
    code = ""
    for _ in range(6):
        code += random.choice(string.ascii_uppercase + string.digits)
    return code


async def getPhoto(user: User):
    bot = Bot(token='8117981299:AAGeYTB606RNqOctq31g3GIWux9qQ4zbQjw')

    photo: UserProfilePhotos = await bot.get_user_profile_photos(user.id)
    if photo.total_count > 0:
        file_id = photo.photos[0][-1].file_id
        file = await bot.get_file(file_id)
        file_url = f'https://api.telegram.org/file/bot{'8117981299:AAGeYTB606RNqOctq31g3GIWux9qQ4zbQjw'}/{file.file_path}'
        return file_url
    else:
        return None


async def getUserPostsCount(user: User):
    db = create_session()
    count = db.query(Posts).filter(Posts.userId == user.id).count()
    db.close()

    return count


async def getPostsRating(user: User):
    db = create_session()
    posts = db.query(Posts).filter(Posts.userId == user.id).all()
    db.close()

    rating = 0
    for post in posts:
        rating += post.rating

    return rating


async def getPost(post_id: str):
    db = create_session()
    post = db.query(Posts).filter((Posts.id == post_id) | (Posts.id.ilike(f'%{post_id}%'))).first()
    db.close()

    return post


async def getPostAuthor(post_id: str):
    db = create_session()
    post = db.query(Posts).filter((Posts.id == post_id) | (Posts.id.ilike(f'%{post_id}%'))).first()
    user = db.query(User).filter(User.id == post.userId).first()
    db.close()

    return user


async def findPost(query: str):
    db = create_session()
    posts = db.query(Posts).filter(
        (Posts.namePost.ilike(f'%{query}%')) |
        (Posts.descPost.ilike(f'%{query}%')) |
        (Posts.id == query)
    ).all()
    db.close()
    return posts


async def deletePost(post_id: str):
    db = create_session()
    post = db.query(Posts).filter(Posts.id == post_id).first()
    images = db.query(ImagePosts).filter(ImagePosts.post_id == post_id).all()
    if post:
        db.delete(post)
        db.commit()

        if images:
            for elem in images:
                db.delete(elem)
        db.commit()
        db.close()

        os.remove(f'templates/posts/{post_id}.html')

        return True
    else:
        return False


async def updatePost(post_id: str, namePost=None, descPost=None, rating=None):
    db = create_session()
    post = db.query(Posts).filter(Posts.id == post_id).first()

    if namePost is not None:
        post.namePost = namePost

    if descPost is not None:
        post.descPost = descPost

    if rating is not None:
        post.rating = rating

    db.commit()
    db.close()


def get_admin_level(session: Session, user_id: int) -> int:
    admin = session.query(Admin).filter(Admin.user_id == user_id).first()
    return admin.level if admin else 0


def require_level(session: Session, user_id: int, required: int) -> bool:
    level = get_admin_level(session, user_id)
    return level >= required


async def getUserCard(user: User):
    def prepare_mask(size, antialias=2):
        mask = Image.new('L', (size[0] * antialias, size[1] * antialias), 0)
        ImageDraw.Draw(mask).ellipse((0, 0) + mask.size, fill=255)
        return mask.resize(size)

    def crop(im, s):
        w, h = im.size
        k = w / s[0] - h / s[1]
        if k > 0:
            im = im.crop(((w - h) / 2, 0, (w + h) / 2, h))
        elif k < 0:
            im = im.crop((0, (h - w) / 2, w, (h + w) / 2))
        return im.resize(s)

    size = (127, 127)

    image = Image.open('data/config/image/card_user.png')

    photo = await getPhoto(user)

    r = requests.get(photo, stream=True)
    p = Image.open(io.BytesIO(r.content))
    n = p.convert('RGBA')
    m = n.resize((127, 127))
    im = crop(m, size)
    im.putalpha(prepare_mask(size, 4))
    im.save('data/config/image/image_output.png', format='png')

    images = Image.open('data/config/image/image_output.png')
    image.paste(images, (43, 68), mask=images)

    idraw = ImageDraw.Draw(image)
    h = ImageFont.truetype('static/font/Montserrat-Bold.ttf', size=50)
    a = ImageFont.truetype('static/font/Montserrat-Regular.ttf', size=35)
    b = ImageFont.truetype('static/font/Montserrat-Bold.ttf', size=38)
    idraw.text((198, 78), f'{user.first_name}', font=h)
    idraw.text((260, 138), f'{user.id}', font=a)
    image.save('data/config/image/card.png')


async def create_report_format(format: str):
    try:
        db = create_session()
        posts = db.query(Posts).all()
        users = db.query(User).all()
        comments = db.query(Comment).all()

        if not posts or not users or not comments:
            return (False, "1")
        if format == 'csv':
            import csv
            with open(f'data/config/report_file.{format}', 'w') as F:
                writerData = csv.writer(F, delimiter=';', dialect='excel')
                writerData.writerow(['Users'])
                writerData.writerow(['ID', "Name", "DataStart"])
                for row in users:
                    writerData.writerow([row.id, row.name, row.dataStart.strftime("%d-%m-%Y %H:%M:%S")])
                writerData.writerow(['\n'])
                writerData.writerow(['Posts'])
                writerData.writerow(['ID', "Name", "DataStart"])
                for row in posts:
                    writerData.writerow([row.id, db.query(User).filter(User.id == row.userId).first().name, row.namePost, row.descPost, row.rating])
                writerData.writerow(['\n'])
                writerData.writerow(['Comments'])
                writerData.writerow(['ID', "Post", "User", "Comment"])
                for row in comments:
                    writerData.writerow([row.id,
                                         db.query(Posts).filter(Posts.id == row.post_id).first().namePost,
                                         db.query(User).filter(User.id == row.user_id).first().name,
                                         row.text])
        else:
            import pandas as pd
            userList = (
                [id.id for id in users],
                [name.name for name in users],
                [data.dataStart.strftime("%d-%m-%Y %H:%M:%S") for data in users]
            )
            postsList = (
                [id.id for id in posts],
                [db.query(User).filter(User.id == row.userId).first().name for row in posts],
                [post.namePost for post in posts],
                [post.descPost for post in posts],
                [row.rating for row in posts]
            )
            commentsList = (
                [id.id for id in comments],
                [db.query(Posts).filter(Posts.id == row.post_id).first().namePost for row in comments],
                [db.query(User).filter(User.id == row.user_id).first().name for row in comments],
                [text.text for text in comments]
            )

            with pd.ExcelWriter(f'data/config/report_file.{format}', engine='openpyxl', mode='w') as writer:
                df = pd.DataFrame({"ID": userList[0], "Имя пользователя": userList[1], "Дата создания": userList[2]})
                df.to_excel(writer, sheet_name='Users', index=False)
                df1 = pd.DataFrame({"ID": postsList[0], "Создатель": postsList[1], "Название поста": postsList[2], "Описание поста": postsList[3], "Рейтинг": postsList[4]})
                df1.to_excel(writer, sheet_name='Posts', index=False)
                df2 = pd.DataFrame({"ID": commentsList[0], "Пост": commentsList[1], "Пользователь": commentsList[2], "Комментарий": commentsList[3]})
                df2.to_excel(writer, sheet_name='Comments', index=False)

        db.close()
        return (True, "0")
    except Exception as e:
        logging.error(f"Ошибка при отправке файла: {traceback.format_exc()}")
        return (False, "2")
