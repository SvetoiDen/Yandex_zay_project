from aiogram import Router, F
from data.func.functions import getUserCard
from aiogram.types import CallbackQuery, Message, WebAppData, FSInputFile

profile = Router()

@profile.callback_query(F.data == 'profile')
async def profileUser(callback: CallbackQuery):
    message = callback.message

    await getUserCard(callback.from_user)
    await callback.answer()
    photo = FSInputFile('data/config/image/card.png')
    await message.answer_photo(photo=photo, caption='Крутой поц')