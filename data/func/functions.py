import string
import random
import asyncio
import traceback
from aiogram.types import User, UserProfilePhotos
from aiogram import Bot
from aiogram.methods import GetUserProfilePhotos
from data.db_data.db_session import create_session
from data.db_data.models.users import User
from data.db_data.models.posts import Posts
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
    post = db.query(Posts).filter(Posts.id == post_id).first()
    db.close()

    return post


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
