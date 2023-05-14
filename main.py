from aiogram.utils import executor
from create_bot import  dp
from handlers import client, admin, other


other.register_handlers_client(dp)
client.register_handlers_client(dp)
# admin.register_handlers_client(dp)



if __name__ == '__main__':
    print('Работаем!')
    executor.start_polling(dp, skip_updates=True)