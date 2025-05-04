import logging

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from data.db_data.db_session import create_session
from data.db_data.models.posts import Posts
from data.db_data.models.users import User
from data.db_data.models.ratings import Ratings

addLike = Router()


@addLike.callback_query(F.data.startswith('like_'))
async def addPostLike(callback: CallbackQuery):
    await callback.answer()
    try:
        postId = callback.data.split("_")[-1]
        db = create_session()

        ratingUser = db.query(Ratings).filter(Ratings.post_id == postId, Ratings.user_id == callback.from_user.id).first()
        post = db.query(Posts).filter(Posts.id == postId).first()
        user = db.query(User).filter(User.id == post.userId).first()

        if ratingUser is not None:
            db.delete(ratingUser)
            post.rating = post.rating - 1
            db.commit()

            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(
                    text="💬 Комментарии", callback_data=f"comments_{post.id}"),
                    InlineKeyboardButton(text='⭐ Поставить лайк', callback_data=f'like_{post.id}')],
                [InlineKeyboardButton(
                    text="🔙 Назад", callback_data="menu")]
            ])

            await callback.message.edit_text(
                f"<b>{post.namePost}</b>\n"
                f"<i>Описание:</i> {post.descPost}\n"
                f"<i>Рейтинг:</i> ⭐ {post.rating}\n"
                f"<i>Автор:</i> 👤 @{user.name}",
                reply_markup=keyboard,
                parse_mode="HTML"
            )
            db.close()
            return

        post.rating = post.rating + 1
        rat = Ratings()
        rat.post_id = post.id
        rat.user_id = user.id
        db.add(rat)
        db.commit()

        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(
                text="💬 Комментарии", callback_data=f"comments_{post.id}"),
                InlineKeyboardButton(text='⭐ Поставить лайк', callback_data=f'like_{post.id}')],
            [InlineKeyboardButton(
                text="🔙 Назад", callback_data="menu")]
        ])

        await callback.message.edit_text(
            f"<b>{post.namePost}</b>\n"
            f"<i>Описание:</i> {post.descPost}\n"
            f"<i>Рейтинг:</i> ⭐ {post.rating}\n"
            f"<i>Автор:</i> 👤 @{user.name}",
            reply_markup=keyboard,
            parse_mode="HTML"
        )
        db.close()
        return
    except Exception as e:
        logging.error(f'Ошибка при добавлении лайка: {e}')
        await callback.message.answer('⚠️ Ошибка при добавлении лайка')
