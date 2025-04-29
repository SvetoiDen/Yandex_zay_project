from sqlalchemy.orm import joinedload
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from data.db_data.db_session import create_session
from data.db_data.models.comments import Comment
from data.db_data.models.posts import Posts
from data.db_data.models.users import User

comment_router = Router()


class CommentStates(StatesGroup):
    waiting_for_comment = State()


@comment_router.callback_query(F.data.startswith("comments_"))
async def open_comments(callback: CallbackQuery, state: FSMContext):
    post_id = callback.data.split("_")[1]
    db = create_session()
    comments = db.query(Comment).options(joinedload(Comment.user))\
        .filter(Comment.post_id == post_id)\
        .order_by(Comment.created_at.asc())\
        .all()

    post = db.query(Posts).filter(Posts.id == post_id).first()
    db.close()

    text = f"💬 Комментарии к посту \"{post.namePost}\":\n\n" if post else f"💬 Комментарии к посту ID {post_id}:\n\n"

    if comments:
        for c in comments:
            text += f"• <b>@{c.user.name}</b>: {c.text}\n"
    else:
        text += "Комментариев пока нет."

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="➕ Добавить комментарий",
                              callback_data=f"add_comment_{post_id}")],
        [InlineKeyboardButton(
            text="🔙 Назад", callback_data=f"open_post_{post_id}")]
    ])

    await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="HTML")
    await callback.answer()


@comment_router.callback_query(F.data.startswith("add_comment_"))
async def ask_comment(callback: CallbackQuery, state: FSMContext):
    post_id = callback.data.split("_")[-1]
    await state.set_state(CommentStates.waiting_for_comment)
    await state.update_data(post_id=post_id)
    await callback.message.answer("📝 Введите ваш комментарий:")
    await callback.answer()


@comment_router.message(CommentStates.waiting_for_comment)
async def save_comment(message: Message, state: FSMContext):
    data = await state.get_data()
    post_id = data["post_id"]

    db = create_session()
    user = db.query(User).filter(User.id == message.from_user.id).first()
    if not user:
        await message.answer("❌ Ошибка: пользователь не найден!")
        db.close()
        return

    comment = Comment(
        post_id=post_id,
        user_id=message.from_user.id,
        text=message.text
    )

    db.add(comment)
    db.commit()
    db.close()

    await state.clear()
    await message.answer("✅ Комментарий добавлен!")
