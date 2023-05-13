from aiogram.types import InlineKeyboardButton

price = InlineKeyboardButton('Рассчитать стоимость заказа🗑', callback_data='price')
new = InlineKeyboardButton('Обновить🗑', callback_data='price')
cancel = InlineKeyboardButton('Отменить🙅‍♂', callback_data='отмена')

back = InlineKeyboardButton('Вернуться в меню🔙', callback_data='menu')


go = InlineKeyboardButton('Всё верно! Отправить заказ✅', callback_data='go')
oki = InlineKeyboardButton('Хорошо✅', callback_data='отмена')
