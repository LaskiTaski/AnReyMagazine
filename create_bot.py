from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from dotenv import load_dotenv
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import os


load_dotenv()
TOKEN_API = os.getenv('TOKEN_API')

storage = MemoryStorage()
bot = Bot(token=TOKEN_API, parse_mode='Markdown')
dp = Dispatcher(bot, storage=storage)

# requests заменить на aiohttp

