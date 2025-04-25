import traceback
from aiogram import Dispatcher, Bot
from cogs import start, profile, openpost, findpost, admin_panel
from data.db_data.db_session import global_init
from server import app
import logging
import asyncio

async def mainTelegram():
    bot = Bot(token='8117981299:AAGeYTB606RNqOctq31g3GIWux9qQ4zbQjw')
    di = Dispatcher()
    logging.basicConfig(level=logging.INFO)

    global_init('data/db_data/db/dbTg.db')

    di.include_routers(start.start, profile.profile, openpost.post, findpost.finder, admin_panel.admin)
    logging.info("Бот запустился.")
    await di.start_polling(bot, skip_updates=True)

async def mainServer():
    context = ('server/cert.pem', 'server/key.pem')
    app.run(host='127.0.0.1', port=5500, ssl_context=context)

if __name__ == '__main__':
    try:
        asyncio.run(mainTelegram())
    except:
        print(traceback.format_exc())
        logging.critical("Бот был выключен")
