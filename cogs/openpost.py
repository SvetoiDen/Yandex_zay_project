from aiogram import Router, F
import logging
from data.func.functions import getPost
from aiogram.types import CallbackQuery
from data.db_data.db_session import create_session
from data.db_data.models.users import User
from data.db_data.models.posts import Posts
from data.func.buttons.buttonTg import postButShow


post = Router()


@post.callback_query(F.data.startswith("open_post_"))
async def open_post_callback(callback: CallbackQuery):
    try:
        post_id = callback.data.split("_")[-1]
        post = await getPost(post_id)

        if post:
            db = create_session()
            user = db.query(User).filter(User.id == post.userId).first()
            db.close()
            await callback.message.answer(
                f"<b>{post.namePost}</b>\n"
                f"<i>Описание:</i> {post.descPost}\n"
                f"<i>Рейтинг:</i> ⭐ {post.rating}\n"
                f"<i>Автор:</i> 👤 @{user.name}",
                reply_markup=postButShow,
                parse_mode="HTML"
            )

        
            await callback.answer()
        else:
            await callback.answer("Пост не найден.")

    except Exception as e:
        logging.error(f"Ошибка при открытии поста: {e}")
        await callback.answer("⚠️ Ошибка при открытии поста.", show_alert=True)
