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


@profile.callback_query(F.data.startswith("profile_page_"))
async def profile_page_callback(callback: CallbackQuery):
    try:
        payload = callback.data.replace("profile_page_", "")
        user_id_str, page_str = payload.rsplit("_", maxsplit=1)
        user_id = int(user_id_str)
        page = int(page_str)

        await callback.message.edit_reply_markup(reply_markup=await getUserPostsButtons(user_id, page))
        await callback.answer()
    except Exception as e:
        logging.error(f"Ошибка при загрузке профиля: {e}")
        await callback.answer("⚠️ Ошибка при загрузке профиля.", show_alert=True)
