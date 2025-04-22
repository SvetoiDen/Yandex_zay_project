from aiogram import Router, F
import logging
from data.func.functions import getUserCard, getUserPostsCount, getPostsRating
from data.func.buttons.buttonTg import getUserPostsButtons
from aiogram.types import CallbackQuery, Message, WebAppData, FSInputFile

post = Router()



@post.callback_query(F.data.startswith("open_post_"))
async def profileUser(callback: CallbackQuery):
    try:
        post_id = int(callback.data.split("_")[-1])
        # тут использовать post_id, например:
        # post = get_post_by_id(post_id)

        # допишу потом



        await callback.answer()

    except Exception as e:
        logging.error(e)
