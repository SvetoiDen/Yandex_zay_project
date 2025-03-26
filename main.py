import traceback
from aiogram import Dispatcher, Bot
from cogs import start, profile
from data.db_data.db_session import global_init
from server import app
import asyncio

async def mainTelegram():
    bot = Bot(token='8117981299:AAGeYTB606RNqOctq31g3GIWux9qQ4zbQjw')
    di = Dispatcher()

    global_init('data/db_data/db/dbTg.db')

    di.include_routers(start.start, profile.profile)
    print('bot on')
    await di.start_polling(bot, skip_updates=True)

async def mainServer():
    context = ('server/cert.pem', 'server/key.pem')
    app.run(host='127.0.0.1', port=5500, ssl_context=context)

if __name__ == '__main__':
    try:
        asyncio.run(mainTelegram())
    except:
        print(traceback.format_exc())
        print('Bot off')