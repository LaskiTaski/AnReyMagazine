from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv
import os
load_dotenv()

TOKEN_API = os.getenv('TOKEN_API')

storage = MemoryStorage()

bot = Bot(token=TOKEN_API,parse_mode='Markdown')

dp = Dispatcher(bot, storage=storage)



from handlers import client, admin, other

client.register_handlers_client(dp)
# admin.register_handlers_client(dp)
other.register_handlers_client(dp)


if __name__ == '__main__':
    print('Работаем!')
    executor.start_polling(dp, skip_updates=True)