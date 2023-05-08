from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv
from handlers import client, admin, other
import os

load_dotenv()

TOKEN_API = os.getenv('TOKEN_API')
storage = MemoryStorage()
bot = Bot(token=TOKEN_API, parse_mode='Markdown')
dp = Dispatcher(bot, storage=storage)


client.register_handlers_client(dp)
# admin.register_handlers_client(dp)
other.register_handlers_client(dp)

async def edit_message(message : str, message_id : int):
    await bot.edit_message_text(message_id=message_id, text=message)


if __name__ == '__main__':
    print('Работаем!')
    executor.start_polling(dp, skip_updates=True)



# git remote add origin https://github.com/LaskiTaski/AnReyMagazine.git
#  git branch -M main
# git push -u origin main