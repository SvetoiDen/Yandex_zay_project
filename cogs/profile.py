from aiogram import Router, F
import logging
from data.func.functions import getUserCard, getUserPostsCount, getPostsRating
from data.func.buttons.buttonTg import getUserPostsButtons
from aiogram.types import CallbackQuery, Message, WebAppData, FSInputFile

profile = Router()


@profile.callback_query(F.data == 'profile')
async def profileUser(callback: CallbackQuery):
    try:
        await getUserCard(callback.from_user)
        posts_count = await getUserPostsCount(callback.from_user)
        rating = await getPostsRating(callback.from_user)




        photo = FSInputFile('data/config/image/card.png')
        caption = (
            f"👤 Профиль пользователя\n"
            f"├ Имя: {callback.from_user.first_name}\n"
            f"├ Лайки: {rating}\n"
            f"└ Посты: {posts_count}"
        )

        await callback.message.answer_photo(
            photo=photo,
            caption=caption,
            reply_markup=await getUserPostsButtons(callback.from_user.id)
        )
        await callback.answer()

    except Exception as e:
        logging.error(e)
        await callback.answer("⚠️ Ошибка при загрузке профиля", show_alert=True)
