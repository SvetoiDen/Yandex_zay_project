import os

from aiogram import Router, F
from aiogram.filters.command import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile
from cogs.admin_panel import check_admin
from data.db_data.db_session import create_session
from data.db_data.models.admins import Admin
from data.func.functions import create_report_format

report = Router()


@report.message(Command('report'))
async def report_panel(message: Message):
    if not await check_admin(message):
        return

    session = create_session()

    admin = session.query(Admin).filter(
        Admin.user_id == message.from_user.id).first()
    if not admin or admin.level < 2:
        return await message.reply("❌ Недостаточно прав.")

    butReport = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text='xlsx', callback_data='xlsx_format'),
        InlineKeyboardButton(text='csv', callback_data='csv_format')]
    ])

    await message.answer(f'Здравствуй, @{message.from_user.username}. Выберите формат файла для отчета', reply_markup=butReport)


@report.callback_query(F.data.endswith('_format'))
async def report_format(callback: CallbackQuery):
    await callback.answer()
    await callback.message.delete()
    dataFormat = callback.data.split('_')[0]

    fileTg = await create_report_format(dataFormat)
    if fileTg[0] and fileTg[1] == "0":
        await callback.message.answer_document(document=FSInputFile(f'data/config/report_file.{dataFormat}'),
                                               caption=f'Вот отчет в формате {dataFormat}')
        os.remove(f'data/config/report_file.{dataFormat}')
    elif fileTg[1] == "2":
        await callback.message.answer(text='⚠️ Ошибка при отправке файла')
    elif fileTg[1] == "1":
        await callback.message.answer(text='⚠️ Нету записей для отчета')
