from aiogram.utils import executor
from create_bot import  dp
from handlers import client, admin, other


client.register_handlers_client(dp)
# admin.register_handlers_client(dp)
other.register_handlers_client(dp)


if __name__ == '__main__':
    print('Работаем!')
    executor.start_polling(dp, skip_updates=True)



# git remote add origin https://github.com/LaskiTaski/AnReyMagazine.git
#  git branch -M main
# git push -u origin main