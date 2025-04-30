import traceback
from aiogram import Dispatcher, Bot
from cogs import start, profile, openpost, findpost, admin_panel, add_comment
from data.db_data.db_session import global_init
from server import app
import logging
import asyncio

async def mainTelegram():
    bot = Bot(token='8117981299:AAGeYTB606RNqOctq31g3GIWux9qQ4zbQjw')
    di = Dispatcher()
    logging.basicConfig(level=logging.INFO)

    global_init('data/db_data/db/dbTg.db')

    di.include_routers(start.start, profile.profile, openpost.post,
                       findpost.finder, admin_panel.admin, add_comment.comment_router)
    logging.info("Бот запустился.")
    await di.start_polling(bot, skip_updates=True)


if __name__ == '__main__':
    try:
        asyncio.run(mainTelegram())
    except:
        print(traceback.format_exc())
        logging.critical("Бот был выключен")
