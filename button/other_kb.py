from aiogram.types import InlineKeyboardButton

price = InlineKeyboardButton('Рассчитать стоимость заказа🗑', callback_data='price')
txt_one = InlineKeyboardButton('О приложении📂', callback_data='txt_one')
txt_two = InlineKeyboardButton('О составлении заказаℹ', callback_data='txt_two')

back = InlineKeyboardButton('Вернуться в меню🔙', callback_data='start')
