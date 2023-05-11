from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

txt_one = InlineKeyboardButton('О приложении📂', callback_data='txt_one')
txt_two = InlineKeyboardButton('О составлении заказаℹ', callback_data='txt_two')
price = InlineKeyboardButton('Рассчитать стоимость заказа🗑', callback_data='price')


back = InlineKeyboardButton('Вернуться в меню🔙', callback_data='menu')
