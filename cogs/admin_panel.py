from data.db_data.models.admins import Admin
from data.func.functions import require_level
from aiogram import Router, F
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery
from aiogram.filters.command import Command
from data.db_data.db_session import create_session
from data.db_data.models.users import User
from data.db_data.models.posts import Posts
from data.func.buttons.buttonTg import postButShow
from aiogram.fsm.context import FSMContext
from data.func.states import AdminStates, EditPostStates
from data.func.functions import getPost, deletePost, updatePost, getPostAuthor
import logging
from sqlalchemy.exc import SQLAlchemyError


admin = Router()
ADMIN_ID = [1012085977, 1099501680]


async def check_admin(message: Message) -> bool:
    if message.from_user.id not in ADMIN_ID:
        await message.answer("❌ У вас нет доступа к админке.")
        return False
    return True


@admin.message(Command("admin"))
async def admin_panel(message: Message):
    if not await check_admin(message):
        return

    await message.answer("🔧 Панель администратора:\n"
                         "/admin - открыть админ панель (1+),\n"
                         "/stats - статистика (1+),\n"
                         "/users - список пользователей (1+),\n"
                         "/edit_post - редактировать пост по ID (2+),\n"
                         "/set_admin - назначить администратора (3+),\n"
                         "/delete_admin - удалить администратора (3+).", reply_markup=postButShow)


@admin.message(Command("stats"))
async def admin_stats(message: Message):
    session = create_session()

    admin = session.query(Admin).filter(
        Admin.user_id == message.from_user.id).first()
    if not admin or admin.level < 1:
        return await message.reply("❌ Недостаточно прав.")

    db = create_session()
    total_users = db.query(User).count()
    total_posts = db.query(Posts).count()
    db.close()

    await message.answer(f"📈 Статистика:\nПользователей: {total_users}\nПостов: {total_posts}")


@admin.message(Command("users"))
async def admin_users(message: Message):
    session = create_session()


    admin = session.query(Admin).filter(
        Admin.user_id == message.from_user.id).first()
    if not admin or admin.level < 1:
        return await message.reply("❌ Недостаточно прав.")

    db = create_session()
    users = db.query(User).all()
    db.close()

    if not users:
        return await message.answer("❌ Нет пользователей.")

    user_list = "\n".join([f"ID: {user.id} - @{user.name}" for user in users])
    await message.answer(f"👥 Список пользователей:\n{user_list}")


@admin.message(Command("edit_post"))
async def admin_edit_post(message: Message, state: FSMContext):
    session = create_session()

    admin = session.query(Admin).filter(
        Admin.user_id == message.from_user.id).first()
    if not admin or admin.level < 2:
        return await message.reply("❌ Недостаточно прав.")
    
    await message.answer("📝 Введите ID поста для редактирования:")
    await state.set_state(AdminStates.waiting_for_post_id)


@admin.message(AdminStates.waiting_for_post_id)
async def admin_handle_post_id(message: Message, state: FSMContext):
    post_id = message.text.strip()
    db_post = await getPost(post_id)

    if not db_post:
        await message.answer(f"❌ Пост с ID {post_id} не найден.")
        await state.clear()
        return

    await state.update_data(post_id=db_post.id)
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="🗑 Удалить", callback_data="admin_delete_post")],
        [InlineKeyboardButton(text="✏️ Редактировать",
                              callback_data="admin_edit_post_text")],
        [InlineKeyboardButton(text="❌ Закрыть", callback_data="admin_cancel")]
    ])
    await message.answer(f"Пост: **{db_post.namePost}**\nВыберите действие:", reply_markup=keyboard, parse_mode="markdown")


@admin.callback_query(F.data == "admin_delete_post")
async def handle_admin_delete(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    post_id = data.get("post_id")

    try:
        db_post = await getPost(post_id)
        if await deletePost(post_id):
            await callback.message.edit_text(f"🗑 Пост **{db_post.namePost}** успешно удален.", parse_mode="markdown")
        else:
            await callback.message.edit_text("❌ Пост не найден.")
    except SQLAlchemyError as e:
        logging.error(f"Database error in admin_delete_post: {e}")
        await callback.message.edit_text("❌ Ошибка при удалении поста.")
    finally:
        await state.clear()
        await callback.answer()


@admin.callback_query(F.data == "admin_edit_post_text")
async def handle_admin_edit(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    post_id = data.get("post_id")

    edit_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✏️ Название",
                                 callback_data=f"edit_title_{post_id}"),
            InlineKeyboardButton(
                text="📝 Описание", callback_data=f"edit_desc_{post_id}")
        ],
        [
            InlineKeyboardButton(
                text="⭐ Рейтинг", callback_data=f"edit_rating_{post_id}"),
            InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_edit")
        ]
    ])

    try:
        db_post = await getPost(post_id)
        db_author = await getPostAuthor(post_id)
        if db_post:
            await callback.message.answer(
                f"<b>Текущий пост:</b>\n"
                f"<b>{db_post.namePost}</b>\n"
                f"<i>Описание:</i> {db_post.descPost}\n"
                f"<i>Рейтинг:</i> ⭐ {db_post.rating}\n"
                f"<i>Автор:</i> 👤 @{db_author.name}\n\n"
                f"<b>Что хотите изменить?</b>",
                reply_markup=edit_keyboard,
                parse_mode="HTML"
            )

    except Exception as e:
        logging.error(f"Database error in admin_edit_post_text: {e}")
        await callback.message.edit_text("❌ Ошибка при редактировании поста.")
        await state.clear()

    finally:
        await callback.answer()



@admin.callback_query(F.data.startswith("edit_title_"))
async def process_edit_title(callback: CallbackQuery, state: FSMContext):
    post_id = callback.data.split("_")[2]
    await state.update_data(post_id=post_id)

    await callback.message.answer(
        "Введите новое название поста:",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[[
            InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_edit")
        ]])
    )
    await state.set_state(EditPostStates.waiting_for_title)
    await callback.answer()


@admin.callback_query(F.data.startswith("edit_desc_"))
async def process_edit_description(callback: CallbackQuery, state: FSMContext):
    post_id = callback.data.split("_")[2]
    await state.update_data(post_id=post_id)

    await callback.message.answer(
        "Введите новое описание поста:",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[[
            InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_edit")
        ]])
    )
    await state.set_state(EditPostStates.waiting_for_description)
    await callback.answer()



@admin.callback_query(F.data.startswith("edit_rating_"))
async def process_edit_rating(callback: CallbackQuery, state: FSMContext):
    post_id = callback.data.split("_")[2]
    await state.update_data(post_id=post_id)

    await callback.message.answer(
        "Введите новый рейтинг поста:",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[[
            InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_edit")
        ]])
    )
    await state.set_state(EditPostStates.waiting_for_rating)
    await callback.answer()



@admin.message(EditPostStates.waiting_for_title)
async def save_new_title(message: Message, state: FSMContext):
    new_title = message.text
    data = await state.get_data()
    post_id = data.get("post_id")

    try:
        await updatePost(post_id, namePost=new_title)
        await message.answer(
            f"✅ Название поста успешно обновлено!\nНовое название: {new_title}",
            parse_mode="HTML"
        )
    except Exception as e:
        logging.error(f"Database error while updating title: {e}")
        await message.answer("❌ Ошибка при обновлении названия поста.")

    await state.clear()



@admin.message(EditPostStates.waiting_for_description)
async def save_new_description(message: Message, state: FSMContext):
    new_description = message.text
    data = await state.get_data()
    post_id = data.get("post_id")

    try:
        await updatePost(post_id, descPost=new_description)
        await message.answer(
            f"✅ Описание поста успешно обновлено!\nНовое описание: {new_description}",
            parse_mode="HTML"
        )
    except Exception as e:
        logging.error(f"Database error while updating description: {e}")
        await message.answer("❌ Ошибка при обновлении описания поста.")

    await state.clear()



@admin.message(EditPostStates.waiting_for_rating)
async def save_new_rating(message: Message, state: FSMContext):
    try:
        new_rating = int(message.text)
        

        data = await state.get_data()
        post_id = data.get("post_id")

        await updatePost(post_id, rating=new_rating)
        await message.answer(
            f"✅ Рейтинг поста успешно обновлен!\nНовый рейтинг: ⭐ {new_rating}",
            parse_mode="HTML"
        )

    except ValueError:
        await message.answer("❌ Пожалуйста, введите числовое значение рейтинга!")
    except Exception as e:
        logging.error(f"Database error while updating rating: {e}")
        await message.answer("❌ Ошибка при обновлении рейтинга поста.")

    await state.clear()



@admin.callback_query(F.data == "cancel_edit")
async def cancel_edit(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("❌ Редактирование отменено.")
    await state.clear()
    await callback.answer()


@admin.callback_query(F.data == "admin_cancel")
async def handle_admin_cancel(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("❌ Действие отменено.")
    await state.clear()
    await callback.answer()


@admin.message(F.text.startswith("/set_admin"))
async def set_admin(message: Message):
    session = create_session()

    try:
        admin = session.query(Admin).filter(
            Admin.user_id == message.from_user.id).first()
        if not admin or admin.level < 3:
            return await message.reply("❌ Недостаточно прав.")

        try:
            _, uid_str, level_str = message.text.split()
            uid = int(uid_str)
            level = int(level_str)
        except:
            return await message.reply("⚠️ Использование: /set_admin <user_id> <уровень (1-3)>")

        target = session.query(Admin).filter(Admin.user_id == uid).first()
        if target:
            target.level = level
        else:
            new_admin = Admin(user_id=uid, level=level)
            session.add(new_admin)

        session.commit()
        await message.reply(f"✅ Назначен уровень {level} для пользователя {uid}")

    except Exception as e:
        session.rollback()
        await message.reply("⚠️ Ошибка при назначении прав.")
    finally:
        session.close()


@admin.message(F.text.startswith("/delete_admin"))
async def delete_admin(message: Message):
    session = create_session()

    try:
        admin = session.query(Admin).filter(
            Admin.user_id == message.from_user.id).first()
        if not admin or admin.level < 3:
            return await message.reply("❌ Недостаточно прав.")

        try:
            _, uid_str = message.text.split()
            uid = int(uid_str)
        except:
            return await message.reply("⚠️ Использование: /delete_admin <user_id>")

        target = session.query(Admin).filter(Admin.user_id == uid).first()
        if not target:
            return await message.reply("⚠️ Администратор с таким ID не найден.")

        session.delete(target)
        session.commit()
        await message.reply(f"✅ Администратор {uid} был удален")

    except Exception as e:
        session.rollback()
        await message.reply("⚠️ Ошибка при снятии прав.")
    finally:
        session.close()
